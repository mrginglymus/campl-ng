var image_styles = require('../../images.json');

describe("Testing responsive images", function() {
  
  
  function test_image_style(image_style_id, image_style) {
    it(image_style.description + " image size", function(done) {
      var _ = this

      browser.url('/core_elements/images')
        .execute(function() {
          return Modernizr.objectfit;
        }).then(function(ret) {
          _.objectFit = ret.value;
        })
        .click("#imagetoggle" + image_style_id)
        .getElementSize('.image-wrapper img').then(function(size) {
          if (size['height'] == 0) {
            expect(size['width']).toEqual(0);
          } else {
            expect(size['height']/size['width']).toBeCloseTo(image_style.height/image_style.width, 2);
          }
        })
        .isVisible('.image-wrapper img').then(function(isVisible) {
          expect(isVisible).toBe(_.objectFit);
        })
        .getElementSize('.image-wrapper').then(function(size) {
          expect(size['height']/size['width']).toBeCloseTo(image_style.height/image_style.width, 2);
        })
        .getCssProperty('.image-wrapper', 'background-image').then(function(bgimage) {
          if (_.objectFit) {
            expect(bgimage['value']).toEqual('none');
          } else {
            expect(bgimage['value']).not.toEqual('none');
          }
        })
        .then(done);
    });
  }
  
  for (image_style in image_styles) {
    test_image_style(image_style, image_styles[image_style]);
  }

});
