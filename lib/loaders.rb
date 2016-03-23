require 'json'

def nested_map_to_sass(src)
  src_json = JSON.parse(File.read(src))
  src_map = {}
  src_json.each do |map_key, map|
    map_map = {}
    map.each do |key, value|
      if value.is_a?(String)
        map_map[Sass::Script::Value::String.new(key)] = Sass::Script::Value::String.new(value)
      else
        map_map[Sass::Script::Value::String.new(key)] = Sass::Script::Value::Number.new(value)
      end
    end
    src_map[Sass::Script::Value::String.new(map_key)] = Sass::Script::Value::Map.new(map_map)
  end
  Sass::Script::Value::Map.new(src_map)
end

module Sass::Script::Functions
  def get_themes
    nested_map_to_sass('./themes.json')
  end
  declare :get_themes, []
  
  def get_images
    nested_map_to_sass('./images.json')
  end
  declare :get_images, []

  def get_fonts
    nested_map_to_sass('./fonts.json')
  end
  declare :get_fonts, []
end