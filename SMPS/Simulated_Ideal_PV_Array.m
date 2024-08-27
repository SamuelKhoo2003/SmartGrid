%% Prep
close all

%% Constants and Preliminary Values
Voc = 5;            %% Open cituit voltage
Isc = 0.23*4;         %% Short circuit current

k = 1.380649e-23; q = 1.602176634e-19; temp = 25; n = 1; numElements = 20;

%% Calculation 1 - Thermal Voltage
T = temp + 273.15;
Vt = k*T/q;

%% Calculation 2 - Reverse Saturation Current
Io = Isc/(exp(round(Voc/(n*Vt), 1))-1);

%% Calculation 3 - Range of Currents to Plot
I = linspace(0, Isc, numElements); % Current range from 0 to Isc

%% Calculate Voltage for Each Current
V = Vt * log((Isc - I) / Io + 1) - I * 0.1; % Adjust Rs as necessary

%% Max Power Point Tracking
max_i = 0; max_v = 0; max_p = 0;

for i=1:numElements
    new_P = I(i)*V(i);
    if new_P>max_p
        max_p = new_P;
        max_i = I(i);
        max_v = V(i);
    end
end

%% Generate Random Error

lower_bound = -0.1;
upper_bound = 0.1;

% Generate random numbers between 0 and 1
random_vector = rand(1, numElements);

% Scale the random numbers to fit the desired range
random_vector = (upper_bound - lower_bound) * random_vector + lower_bound;
newI = I+ random_vector;

%% Plot the I-V Curve
figure;
hold on;
plot(V, I        , 'LineWidth',2, 'Color','r');
plot(V, newI, '*', 'LineWidth',2, 'Color',[0,0.7,0.9]);
hold off;

xlabel('Voltage (V)');
ylabel('Current (I)');
xlim([4.75 5]);
title('I-V Curve of the PV Cell');
legend('Ideal','"Measured"');
grid on;

%% Write Data to Excel

% Combine vectors into a matrix
dataMatrix = [V',I',newI'];

% Write the matrix to Excel
writematrix(dataMatrix, 'myData.xlsx', 'Sheet', 'Sheet1', 'Range', 'A1');
