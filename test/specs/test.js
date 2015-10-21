var webdriverio = require('webdriverio');
var options = require('../wdio.conf').config;
var client = webdriverio.remote(options).init();


describe("this is my test suite", function() {

  var client = {}

  beforeEach(function(done) {
    client = webdriverio.remote(options);
    client.init(done);
  });

  it("this is my test spec", function() {
    a = true;
    expect(a).toBe(true);
  });

  afterEach(function(done) {
    client.end(done);
  });
});


client
  .init()
  .url('/')
  .getTitle(function(err, title) {
    console.log('hi');
    console.log(err);
    console.log(title);
  })
  .end();
