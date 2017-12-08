function  [fdelta, h] = find_fdelta()
    y = read_file();
    y_square = y.^2;
    fft_y2 = abs(fftshift(fft(y_square)));
    figure
    plot(fft_y2); % impulse has index of 2fdelta and area h^2
    [h_sq, idx] = max(fft_y2)
    fdelta = idx/2;
    h = sqrt(h_sq);
    
    for n=1:length(y)
        y(n) = y(n) / (h * exp(1i*fdelta*n));
     end
    
    figure
    plot(y); % second eye
end
function y = read_file()
    f1 = fopen('transmissiontest.dat', 'r');
    tmp = fread(f1,'float32');
    fclose(f1);
    y = tmp(1:2:end)+1i*tmp(2:2:end);
    plot(y); % original eye
end