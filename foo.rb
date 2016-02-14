require 'sass'

file = 'scss/primefaces/structure/base/panel/panel.scss'

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
    base_rule_name = '$' + node.resolved_rules.to_s.gsub(/[ .,#&:]/, '_')
    node.children.each do |child|
    	rule_name = base_rule_name + '___' + child.resolved_name.gsub(/[*]/, '_');
    	variables << Rule.new(child.line, rule_name, child.resolved_value)
    end
  end
end

File.open(file, 'r+') do |f|
	f.each_with_index do |line, idx|
		variables.each do |variable|
			if idx + 1 == variable.line
				puts line
				puts line.sub(variable.value, variable.variable)
			end
		end
	end
end