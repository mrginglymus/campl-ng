describe("Testing responsive images", function() {


  it("Leading image size", function(done) {
    browser.url('/core_elements/images/')
      .pause(1000)
      .getElementSize('.image-wrapper img').then(function(size) {
        if (size['height'] == 0) {
          expect(size['width']).toEqual(0);
        } else {
          expect(size['height']/size['width']).toBeCloseTo(288/590, 2);
        }
      })
      .then(done);
  });


});
