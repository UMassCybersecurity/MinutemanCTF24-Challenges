STRING = int8('MINUTEMAN{ThE_brITish_r_COMing}');
%STRING = int8('What_did_the_ocean_say_to_the_sand__nothing_it_just_waved');
REPITITIONS = 10;
NOISE_SCALE = 0.5;
FILE_NAME = "message.wav";
% Reserve space for data
data_bits = zeros(length(STRING) * 8 * REPITITIONS, 1);
% Copy string bits into the data multiple times
for i = 1:length(STRING) * 8:length(data_bits)
    data_bits(i:(i - 1) + length(STRING) * 8) = char2bin(STRING);
end
% Encode into bpsk symbols
bpsk_symbols = data_bits * 2 - 1;
% Makecomplex noise by picking a direction uniformly, then a magnitude from
% the standard normal distribution
noise = exp(2 * pi * 1i * rand(length(bpsk_symbols), 1)) .* randn(length(bpsk_symbols), 1);
% Add noise with scale factor
bpsk_symbols_with_noise = bpsk_symbols + NOISE_SCALE * noise;
% Rescale to [-1, 1] for audiowrite
scaled = rescale(real(bpsk_symbols_with_noise), -1 , 1);
audiowrite(FILE_NAME, scaled, 1);

% Sample solve script
recovered_samples = audioread(FILE_NAME);
recovered_bits = zeros(length(recovered_samples), 1);

for i = 1:length(recovered_bits)
    if recovered_samples((i - 1) + 1) < 0
        recovered_bits(i) = 0;
    else
        recovered_bits(i) = 1;
    end
end

disp(bin2char(recovered_bits));

% Using matlab
disp(bin2char(not(pskdemod(recovered_samples, 2))));
