<?php

// genicon.php - Code to generate license icon button images.
// Copyright 2016 Creative Commons Corporation.

////////////////////////////////////////////////////////////////////////////////
// Graphics
////////////////////////////////////////////////////////////////////////////////

function alphaValue($hex) {
    // Alpha is 0 (opaque) .. 127 (transparent) because why not.
    // Convert 0 (transparent) .. 255 (opaque) to this.
    $dec = hexdec($hex);
    $inverse = 255 - $dec;
    $scaled = floor($inverse / 2);
    return $scaled;
}

// Only accept rgb/rgba 6 or 8 digit hex color descriptions
function allocate_color ($img, $spec) {
    $elements = str_split($spec, 2);
    $num_elements = count($elements);
    if ($num_elements < 3 || $num_elements > 4) {
        exit(1);
    }
    // Assume opaque
    if ($num_elements == 3) {
        $elements[] = 'ff';
    }
    return imagecolorallocatealpha($img,
                                   hexdec($elements[0]),
                                   hexdec($elements[1]),
                                   hexdec($elements[2]),
                                   alphaValue($elements[3]));
}

////////////////////////////////////////////////////////////////////////////////
// Draw the image (main flow of execution)
////////////////////////////////////////////////////////////////////////////////


// Create the image

function createImage ($width, $height) {
    $im = imagecreatetruecolor($width, $height);
    imagesavealpha($im, true);
    return $im;
}

function drawBackground ($im, $background) {
    if ($background == 'transparent') {
        $background_color = imagecolorallocatealpha($im, 0, 0, 0, 127);
    } else {
        $background_color = allocate_color($im, $background);
    }
    imagefill($im, 0, 0, $background_color);
}

/*function drawIcons ($im, $font, $font_size, $icon_spacing, $foreground,
   $module_chars) {
    $color = allocate_color($im, $foreground);
    $font_size = floor(imagesy($im) / 1.5);
    $bounds = imagettfbbox($font_size, 0, $font, $module_chars);
    $text_width = $bounds[2] - $bounds[0];
    $text_height = $bounds[7] - $bounds[1];
    // x and y are integer, and we're dealing with comparatively small images
    // so use some rounding hacks to try and make sure things end up high and
    // to the left when we can't align them perfectly.
    $x = ceil(imagesx($im) / 2) - floor($text_width / 2);
    $y = floor(imagesy($im) / 2) - ceil($text_height / 2);
    imagettftext($im, $font_size, 0, $x, $y, $color, $font, $module_chars);
}*/


function drawIcons ($im, $font, $font_size, $font_y, $icon_spacing, $foreground,
                    $module_chars) {
    $color = allocate_color($im, $foreground);
    $num_chars = strlen($module_chars);
    // Text height is the maximum of every character
    $bounds = imagettfbbox($font_size, 0, $font, $module_chars);
    $text_height = $bounds[7] - $bounds[1];
    // Text width is the sum of every character's width displayed individually
    // This is different from the width of the string containing them.
    ///$text_width = 0;
    //foreach (str_split($module_chars) as $module) {
    //    $module_bounds = imagettfbbox($font_size, 0, $font, $module);
    //    $text_width += $module_bounds[2] - $module_bounds[0];
    //}
    // Some chars have different spacing. Ignore this.
    $first_char_bounds = imagettfbbox($font_size, 0, $font, $module_chars[0]);
    $text_width = ($first_char_bounds[2] - $first_char_bounds[0]) * $num_chars;
    $total_spacing = $icon_spacing * ($num_chars - 1);
    // x and y are integer, and we're dealing with comparatively small images
    // so use some rounding hacks to try and make sure things end up high and
    // to the left when we can't align them perfectly.
    $x = ceil((imagesx($im) / 2) - floor($text_width / 2))
              - floor($total_spacing / 2);
    $y = $font_y; //floor(imagesy($im) / 2) - ceil($text_height / 2);
    foreach (str_split($module_chars) as $module) {
        $char_bounds = imagettftext($im, $font_size, 0, $x, $y, $color, $font,
                               $module);
        $x += ($char_bounds[2] - $char_bounds[0]) + $icon_spacing;
    }
}

// Caller owns the image

function genicon ($modules, $font, $font_size, $font_y, $icon_spacing,
                  $width, $height, $background, $foreground) {
    global $modules_to_chars;
    $im = createImage ($width, $height);
    drawBackground($im, $background);
    drawIcons($im, $font, $font_size, $font_y, $icon_spacing, $foreground,
              $modules);
    return $im;
}
