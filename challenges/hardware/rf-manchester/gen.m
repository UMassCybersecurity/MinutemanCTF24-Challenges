FLAG = 'YOU MAKE UP YOUR OWN TRUTH';

CARRIER_FREQ1 = 1000; % cycles / second
CARRIER_FREQ2 = 3000; % cycles / second
SAMPLE_RATE = 10000; % samples / second
TIME_UNIT = 0.2; % seconds
NUM_PADDING = 5;

ONE = sin(0:2*pi/(SAMPLE_RATE/CARRIER_FREQ1):2*pi*CARRIER_FREQ1*TIME_UNIT - 2*pi/(SAMPLE_RATE/CARRIER_FREQ1));
ZERO = sin(0:2*pi/(SAMPLE_RATE/CARRIER_FREQ2):2*pi*CARRIER_FREQ2*TIME_UNIT - 2*pi/(SAMPLE_RATE/CARRIER_FREQ2));

binaryData = char2bin(FLAG);

data = zeros(1, length(ONE) * (length(binaryData) + NUM_PADDING));
index = NUM_PADDING * length(ONE) + 1;
for i = 1:length(binaryData)
    if binaryData(i) == 0
        data(index:index + length(ONE) - 1) = ZERO;
        index = index + length(ONE);
        data(index:index + length(ONE) - 1) = ONE;
        index = index + length(ONE);
    else
        data(index:index + length(ONE) - 1) = ONE;
        index = index + length(ONE);
        data(index:index + length(ONE) - 1) = ZERO;
        index = index + length(ONE);
    end
end

audio = audioplayer(data, 10000);
play(audio);

audiowrite('two.wav', data, 10000);