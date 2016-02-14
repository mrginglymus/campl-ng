require 'sass'

file = ARGV[0]

class Rule
	attr_accessor :line, :variable, :value

	def initialize(line, variable, value)
		@line = line
		@variable = variable
		@value = value
	end
end

sass_engine = Sass::Engine.for_file(file, {
	:syntax => :scss,
})

tree = sass_engine.to_tree

Sass::Tree::Visitors::CheckNesting.visit(tree)
result = Sass::Tree::Visitors::Perform.visit(tree)
Sass::Tree::Visitors::CheckNesting.visit(result)
result, extends = Sass::Tree::Visitors::Cssize.visit(result)
Sass::Tree::Visitors::Extend.visit(result, extends)

variables = Array.new

result.each do |node|
  if node.is_a? Sass::Tree::RuleNode
    base_rule_name = '$' + node.resolved_rules.to_s.gsub(/\W/, '_')
    node.children.each do |child|
    	rule_name = base_rule_name + '___' + child.resolved_name.gsub(/\W/, '_');
    	variables << Rule.new(child.line, rule_name, child.resolved_value)
    end
  end
end



text = File.readlines(file)
text.each_with_index do |line, idx|
	variables.each do |variable|
		if idx + 1 == variable.line
			text[idx] = line.sub(variable.value + ';', variable.variable + ';')
		end
	end
end

variablesArray = Array.new

variables.each do |variable|
	variablesArray << variable.variable + ': ' + variable.value + ' !default;'
end

File.open(file, 'w') do |f|
	f.puts variablesArray
	f.puts text
end







