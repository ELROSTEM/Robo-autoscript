%Reads the image
img = imread('WaterBottle.jpg');
%Creates a mask using the Image Segmentation app
mask = segmentImage(img);
[numRows, numCols] = size(mask);
mask = mask(numRows/2, :);
line = mask;
%Makes sure the first/last element of the array is not 0
line = [1 , line , 1];
i = 1;
current = [];
total = [];
counter = [];
%Main while loop,
%Finds the largest distance between black tiles 
%% Note: This is inverse, it needs to find largest distance between white tiles
while i < length(line)+1
    if line(1, i) == 0
        if line(1, i-1) == 1 %If there is a white tile before it
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
imshow(img)

