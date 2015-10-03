require 'json'

module Sass::Script::Functions
  def get_themes
    themes = JSON.parse(File.read('./themes.json'))
    themes_map = {}
    themes.each do |variant_name, variant|
      sass_map = {}
      variant.each do |key, value|
        sass_map[Sass::Script::Value::String.new(key)] = Sass::Script::Value::String.new(value)
      end
      themes_map[Sass::Script::Value::String.new(variant_name)] = Sass::Script::Value::Map.new(sass_map)
    end
    Sass::Script::Value::Map.new(themes_map)
  end
  declare :get_themes, []
end