image_styles = require('../../images.json')

describe 'Testing responsive images', ->

  test_image_style = (image_style_id, image_style) ->
    it "#{image_style.description} image size", (done) ->
      browser.url '/core_elements/images'
        .pause 1000
        .execute ->
          Modernizr.objectfit
        .then (ret) =>
          @objectFit = ret.value
        .getAttribute '.image-wrapper img', 'src'
        .then (src) =>
          @src = src
        .click "#imagetoggle#{image_style_id}"
        .getElementSize '.image-wrapper img'
        .then (size) ->
          if size.height is 0
            expect size.width
              .toEqual 0
          else
            expect size.height / size.width
              .toBeCloseTo image_style.height / image_style.width, 2
        .isVisible '.image-wrapper img'
        .then (isVisible) =>
          expect isVisible
            .toBe @objectFit
        .getElementSize '.image-wrapper'
        .then (size) ->
          expect size.height / size.width
            .toBeCloseTo image_style.height / image_style.width, 2
        .getCssProperty '.image-wrapper', 'background-image'
        .then (bgimage) =>
          if @objectFit
            expect bgimage.value
              .toEqual 'none'
          else
            expect bgimage.value
              .toEqual "url(\"#{@src}\")"
        .then done

  for image_style_id, image_style of image_styles
    test_image_style image_style_id, image_style
