function y = decimate1(x,m)
     % part of the code in this function is taken from
     % https://tomroelandts.com/articles/how-to-create-a-simple-low-pass-filter
     
     fc = 0.4; % Cutoff frequency as a fraction of the sampling rate (in (0, 0.5)).
     b = 0.08; % Transition band, as a fraction of the sampling rate (in (0, 0.5)).
     N = ceil(4/b);
     
     if mod(N,2) ~= 0
         N = N+1; % Make sure that N is odd.
     end
     
     n = 0:N-1;
     % Compute sinc filter.
     h = sinc(2 * fc * (n - (N - 1) / 2.));
     % Compute Blackman window.
     w = hamming(N);
     % Multiply sinc filter with window.
     h = h * w;
     % Normalize to get unity gain.
     h = h / sum(h);
     % Applying filter to the input signal
     x = conv(x,h);
     % Downsampling
     y = x(1:m:end);
end    