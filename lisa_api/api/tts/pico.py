from lisa_api.api.tts import base
from subprocess import call
from pydub import AudioSegment
import tempfile
import logging
logger = logging.getLogger('lisa_api')


class Pico(base.TTSBase):
    """Use picotts
    """

    def convert(self, message, lang="en"):
        """Convert the text to sound and return this sound.

        :param message: A string containing the message
        :type message: str
        :param lang: The lang to use
        :type lang: str
        :returns: Audio data.
        """
        combined_sound = []

        tempwav = tempfile.NamedTemporaryFile(suffix=".wav")
        tempmp3 = tempfile.NamedTemporaryFile(suffix=".mp3")
        print lang

        if 'en' in lang:
            language = 'en-US'
        else:
            language = '-'.join([str(lang), str(lang).upper()])
        command = ['pico2wave', '-w', tempwav.name, '-l', language, '--', message]
        try:
            logger.debug("Command used to generate the sound : %s in the file %s" % (command, tempwav.name))
            call(command)
        except OSError:
            logger.err('OSError exception')
            return False

        sound = AudioSegment.from_wav(tempwav.name)
        sound.export(tempmp3, format="mp3", bitrate="256k")
        tempwav.close()
        combined_sound.append(tempmp3.read())
        tempmp3.close()
        return ''.join(combined_sound)
