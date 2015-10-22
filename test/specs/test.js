var webdriverio = require('webdriverio');

describe("this is my test suite", function() {



  it("this is my test spec", function(done) {
    a = true;
    expect(a).toBe(true);
    browser.url('/')
      .getTitle(function(err, title) {
        expect(title).toBe('CamPL-NG: Home');
        done();
      });
  });


});
