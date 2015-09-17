<?php

global $base_url;

$base_theme_path = base_path() . drupal_get_path('theme', 'cambridge_theme');

$site_title = !empty($section_title) ? $section_title : $site_name;

$has_carousel = isset($page['carousel']) && count($page['carousel']);
$has_left_navigation = isset($page['left_navigation']) && count($page['left_navigation']);
$has_page_title = !$is_front && !$has_carousel && $title && $title != '' && ($has_left_navigation || $title !== $site_title);
$has_sub_content = isset($page['sub_content']) && count($page['sub_content']);
$has_sidebar = (isset($page['sidebar']) && count($page['sidebar'])) || $has_carousel;
$has_partnerships = isset($page['partnerships']) && count($page['partnerships']);

?>

{% include 'drupal/lib/global_header.html' %}
