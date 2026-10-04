require 'xcodeproj'

root = '/private/tmp/shopdiscover-native-checks'
project = Xcodeproj::Project.new("#{root}/NativeChecks.xcodeproj")
target = project.new_target(:ui_test_bundle, 'NativeChecks', :ios, '15.1')
target.add_file_references([project.main_group.new_file("#{root}/NativeFlowTests.swift")])
target.build_configurations.each do |config|
  config.build_settings['PRODUCT_BUNDLE_IDENTIFIER'] = 'local.shopdiscover.NativeChecks'
  config.build_settings['GENERATE_INFOPLIST_FILE'] = 'YES'
  config.build_settings['SWIFT_VERSION'] = '5.0'
  config.build_settings['CODE_SIGNING_ALLOWED'] = 'NO'
end
project.save
scheme = Xcodeproj::XCScheme.new
scheme.add_build_target(target)
scheme.add_test_target(target)
scheme.save_as(project.path, 'NativeChecks', true)
