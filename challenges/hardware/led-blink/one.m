FLAG = 'YOU WANT TO BE FOOLED';

CARRIER_FREQ = 1000; % cycles / second
SAMPLE_RATE = 10000; % samples / second
TIME_UNIT = 0.2; % seconds

DIT = sin(0:2*pi/(SAMPLE_RATE/CARRIER_FREQ):2*pi*CARRIER_FREQ*TIME_UNIT - 2*pi/(SAMPLE_RATE/CARRIER_FREQ));
DAH = [DIT DIT DIT];
GAP = zeros(1, length(DIT));
LETTER_GAP = [GAP GAP GAP];
WORD_GAP = [GAP GAP GAP GAP GAP GAP GAP];

morse = {'.----','..---','...--','....-','.....','-....','--...','---..','----.','-----','.-','-...','-.-.','-..','.','..-.','--.','....','..','.---','-.-','.-..','--','-.','---','.--.','--.-','.-.','...','-','..-','...-','.--','-..-','-.--','--..'}; 
symbol = ['1','2','3','4','5','6','7','8','9','0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];

data = [LETTER_GAP];
words = split(FLAG, ' ');
for i = 1:length(words)
    word = words{i};
    for j = 1:length(word)
        code = morse{symbol == word(j)};
        for k = 1:length(code)
            if code(k) == '.'
                data = [data DIT];
            elseif code(k) == '-'
                data = [data DAH];
            end
            data = [data GAP];
        end
        data = [data LETTER_GAP];
    end
    data = [data WORD_GAP];
end

audio = audioplayer(data, 10000);
play(audio);

audiowrite('one.wav', data, 10000);