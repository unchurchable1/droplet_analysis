// Open image from arguments if available
var closeWindow = false;
if (lengthOf(getArgument()) > 0) {
	// Open the image
	open(getArgument(), "virtual");
	closeWindow = true;
}

// Set the appropriate scale
pixelWidth = getWidth();
umInAPixel = 2.87;
knownDistance = pixelWidth * umInAPixel;
run("Set Scale...", "distance=pixelWidth known=knownDistance unit=microns");

// Subtract background from image stack
run("Subtract Background...", "rolling=10 light stack");

// Generate a binary image from our image stack
setOption("BlackBackground", false);
run("Convert to Mask", "method=Default background=Light");
run("Fill Holes", "stack");
// Try to separate blobs into individual chromophores
run("Watershed", "stack");
saveAs("tif", "droplets/images/" + File.getName(getTitle()));

// Generate ROIs
run("Set Measurements...", "area centroid perimeter fit shape feret's stack redirect=None decimal=3");
run("Analyze Particles...", "size=33-Infinity circularity=0.50-1.00 show=Overlay display exclude include add stack");
roiManager("Show None");
saveAs("Results", "droplets/results/Results_" + File.getNameWithoutExtension(getTitle()) + ".csv");

// Close ImageJ window when running in batches
if (closeWindow) {
	run("Quit");
}
