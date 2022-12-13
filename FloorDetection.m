%Reads the image
img = imread('WaterBottle.jpg');
%Creates a mask using the Image Segmentation app
mask = segmentImage(img);
[numRows, numCols] = size(mask);
mask = mask(numRows/2, :);
line = mask;
%Makes sure the first/last element of the array is not 0
line = [0 , line , 0];
i = 1;
current = [];
total = [];
counter = [];
%Main while loop,
%Finds the largest distance between black tiles 
%% Note: This is inverse, it needs to find largest distance between white tiles
while i < length(line)+1
    if line(1, i) == 1
        if line(1, i-1) == 0 %If there is a white tile before it
                total = [total, current]; 
                current = 1;
                counter = [counter, i];
        else %If there is a black tile before it
            current = current + 1;
            counter = [counter, i];
        end
    end 
    i = i + 1;
end
total = [total, current];
[a,b] = max(total);
%Possibly pointless mat2cell and back to cell2mat
c = mat2cell(counter', total); 
c = cell2mat(c(b));
%Draws the line at the end
for j = 1:j+1
    img = insertShape(img, 'line', [min(c) 1000 max(c) 1000], 'LineWidth', 10, 'Color', 'red');
end
%Draws the circle in the center of the line
img = insertShape(img,"circle",[mean(c) 1000 1],LineWidth=25);
%imshow(img)
%Drawing temporary lines for viewing the division of the screen
img = insertShape(img, 'line', [7*numCols/16 0 7*numCols/16 numRows], 'LineWidth', 10, 'Color', 'blue');
img = insertShape(img, 'line', [9*numCols/16 0 9*numCols/16 numRows], 'LineWidth', 10, 'Color', 'blue');
img = insertShape(img, 'line', [7*numCols/32 0 7*numCols/32 numRows], 'LineWidth', 10, 'Color', 'blue');
img = insertShape(img, 'line', [25*numCols/32 0 25*numCols/32 numRows], 'LineWidth', 10, 'Color', 'blue');

imshow(img)
%if the line is less than x pixels then say there is no free space
%try specifying angle 

if mean(c) < 7*numCols/32
    %disp("1st segment")
    disp("Turn left and go forwards")
elseif mean(c) > 7*numCols/32 & mean(c) < 7*numCols/16 
    %disp("2nd segment")
    disp("Turn slightly left and go forwards")
elseif mean(c) > 7*numCols/16 & mean(c) < 7*numCols/32
    %disp("3rd segment")
    disp("Go forwards")
elseif mean(c) > 7*numCols/32 & mean(c) < 25*numCols/32
    %disp("4th segment")
    disp("Turn slightly right and go forwards")
elseif mean(c) > 25*numCols/32
    %disp("5th segment")
    disp("Turn right and go forwards")
end