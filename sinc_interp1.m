function y = sinc_interp1(x,k)
    [n,m] = size(x);
    nn = n*k;
    xt = linspace(1, n, n);
    xp = linspace(1, n, nn);
    s = size(xp);
    y = zeros(s);
    
    for i=1:length(xp)
        si = repmat(sinc(xt - xp(i)), m, 1);
        dot = si*x;
        y(:,i) = sum(dot);
    end
end