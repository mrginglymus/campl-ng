var image_styles = require('../../images.json');

describe("Testing responsive images", function() {
  
  for (var image_style in image_styles) {
    it(image_styles[image_style].description + " image size", function(done) {
      browser.url('/core_elements/images/')
        .click("#imagetoggle" + image_style)
        .getElementSize('.image-wrapper img').then(function(size) {
          if (size['height'] == 0) {
            expect(size['width']).toEqual(0);
          } else {
            expect(size['height']/size['width']).toBeCloseTo(image_styles[image_style].height/image_styles[image_style].width, 2);
          }
        })
        .then(done);
    });
  }

});
