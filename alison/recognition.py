import numpy as np
import alison.nmf as nmf
from alison.spectrum import get_stft
from alison.signal_alignment import verif_lines


class SoundEvent:
    def __init__(self, time, tag, value, color="no_color"):
        self.time = time
        self.tag = tag
        self.value = value
        self.color = color


class TagInfo:
    def __init__(self, components_range, best_line, best_line_index, color="no_color"):
        self.components_range = components_range
        self.activated = False
        self.best_line = best_line
        self.best_line_index = best_line_index
        self.color = color


class SoundRecognizer:
    def __init__(self, **kwargs):
        self.threshold = 10
        self.horizon = 20
        self.components_per_tag = 3
        # sample rate in hertz
        self.sample_rate = 25

        self.tags = {}
        # shape: [n_features, n_components]
        self.dictionary = None
        self.activations = None

        # current_audio contains the audio that was recorded but not yet parsed.
        self.current_position = 0
        self.current_audio = np.array([])
        # shape: [n_components, time]
        self.current_nmf_results = np.array([])

        # == Results
        # events are for example when a sound started to play
        self.events = []
        self.callback = kwargs["callback"] if "callback" in kwargs else None

    def _component_count(self):
        return self.dictionary.shape[1]

    def _reset_sound_processing(self):
        self.current_position = 0
        self.current_audio = np.array([])
        self.current_nmf_results = np.zeros([self._component_count(), 0])

        self.events = []


    """ Get the index of the activaiton line with the greatest sum of values"""
    def best_activation_line(self):
        maxIndex = -1
        maxValue = 0
        for i in range(self.components_per_tag) :
            sumLine = sum(self.activations[i, :])
            if (sumLine > maxValue):
                maxIndex = i
                maxValue = sumLine
        return maxIndex


    def add_dictionary_entry(self, tag, color, entry):
        """Add a sound to be recognized by Big Alison.

        entry: a sound sample containing mostly the sound to recognize."""
        stft = get_stft(entry / 1.0)
        dico, _ = nmf.get_nmf(stft, self.components_per_tag)
        activations = nmf.get_activations(stft, dico, self.components_per_tag)
        if self.dictionary is None:
            self.dictionary = dico
            self.activations = activations
        else:
            self.dictionary = np.concatenate((self.dictionary, dico), axis=1)
            self.activations = activations

        range_stop = self.dictionary.shape[1]
        range_start = range_stop - dico.shape[1]
        index = self.best_activation_line()
        self.tags[tag] = TagInfo(range(range_start, range_stop), activations[index, :], index, color)

        self._reset_sound_processing()

    def save_dictionary(self, filename):
        """Save the dictionary to a file.
        Then the dictionary can be loaded with self.load_dictionary"""
        file = open(filename, 'w')
        file.write(str(self.dictionary.shape[0]))
        file.write(" ")
        file.write(str(self.dictionary.shape[1]))
        file.write("\n")

        file.write(str(len(self.tags)))
        file.write("\n")

        for key, value in self.tags.items():
            file.write(key.replace(" ", "_"))
            file.write(" ")
            file.write(str(value.components_range.start))
            file.write(" ")
            file.write(str(value.components_range.stop))
            file.write(" ")
            file.write(str(value.best_line_index))
            file.write("\n")

        for l in range(0, self.dictionary.shape[0]):
            for c in range(0, self.dictionary.shape[1]):
                file.write(str(self.dictionary[l, c]))
                file.write(" ")

            file.write("\n")

        file.close()

    def load_dictionary(self, filename):
        """Load the reference dictionary from a file"""
        file = open(filename, 'r')
        lines = file.readlines()

        shapestr = lines[0].split(" ")
        self.dictionary = np.zeros([int(shapestr[0]), int(shapestr[1])])

        tag_count = int(lines[1])

        for i in range(0, tag_count):
            tag_str = lines[i + 2].split(" ")
            self.tags[tag_str[0]] = TagInfo(
                range(int(tag_str[1]), int(tag_str[2])), int(tag_str[3]))

        for l in range(0, self.dictionary.shape[0]):
            linestr = lines[l + 2 + tag_count].split(" ")

            for c in range(0, self.dictionary.shape[1]):
                self.dictionary[l, c] = float(linestr[c])

        self._reset_sound_processing()

    def save_activations(self, filename):
        """Save the activations lines to a file.
        Then the activations lines can be loaded with self.load_activations"""
        file = open(filename, 'w')
        file.write(str(self.activations.shape[0]))
        file.write(" ")
        file.write(str(self.activations.shape[1]))
        file.write("\n")

        file.write(str(len(self.tags)))
        file.write("\n")

        for key, value in self.tags.items():
            file.write(key.replace(" ", "_"))
            file.write(" ")
            file.write(str(value.components_range.start))
            file.write(" ")
            file.write(str(value.components_range.stop))
            file.write(" ")
            file.write(str(value.best_line_index))
            file.write("\n")

        for l in range(0, self.activations.shape[0]):
            for c in range(0, self.activations.shape[1]):
                file.write(str(self.activations[l, c]))
                file.write(" ")

            file.write("\n")

        file.close()

    def load_activations(self, filename):
        """Load the reference activation matrix from a file"""
        file = open(filename, 'r')
        lines = file.readlines()

        shapestr = lines[0].split(" ")
        self.activations = np.zeros([int(shapestr[0]), int(shapestr[1])])

        tag_count = int(lines[1])

        for l in range(0, self.activations.shape[0]):
            linestr = lines[l + 2 + tag_count].split(" ")

            for c in range(0, self.activations.shape[1]):
                self.activations[l, c] = float(linestr[c])

        self._reset_sound_processing()

    def process_audio(self, audio):
        """Compute spectrum from audio source, and call process_spectrum with
        the result"""
        self.current_audio = np.concatenate((self.current_audio, audio))
        spectrum = get_stft(self.current_audio)
        if spectrum.size > 0:
            self.process_spectrum(spectrum)

        # current functions parse the whole audio, so we let nothing in current_audio
        # (parsing the whole data regardless of its size, may result in artifacts
        # in the reconstructed spectrum)
        self.current_audio = np.array([])

    def process_spectrum(self, spectrum):
        """Compute NMF and detect events from the results.
        Mean is computed over `horizon` at each sample and the tag is activated if one
        of the components is greater than `threshold`"""
        if self.dictionary is None:
            return

        activations = nmf.get_activations(spectrum, self.dictionary)
        self.current_nmf_results = np.concatenate((self.current_nmf_results, activations), axis=1)
        parsed_size = self.current_nmf_results.shape[1] - self.horizon

        for tag, tag_info in self.tags.items():
            value = verif_lines(tag_info.best_line, activations[tag_info.best_line_index + tag_info.components_range.start, :])
            activated = value > 0.7
            print(value)
            if activated:
                event = SoundEvent(
                    self.current_position / self.sample_rate,
                    tag, value,tag_info.color)
                self.events.append(event)

                if self.callback is not None:
                    self.callback(event)


        self.current_position += parsed_size
        self.current_nmf_results = self.current_nmf_results[:, -self.horizon:]
