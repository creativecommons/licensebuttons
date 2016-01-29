<?php
// foregrounds.php - Code to generate a long list of colors for the foreground.
// Copyright 2016 Creative Commons Corporation.

// Web safe colours by name

// X11 colours by name

// HTML colours by name

// Generate 256 greys

function greys () {
    return array_map(function($x){ return str_repeat(sprintf("%02X", $x), 3); },
                     range(0, 255));
}

// Generate 24-bit colors, stride 8

function colors () {
    $colors = [];
    foreach (range(0, 255, 8) as $r) {
        foreach (range(0, 255, 8) as $g) {
            foreach (range(0, 255, 8) as $b) {
                $colors[] = sprintf("%02X%02X%02X", $r, $g, $b);
            }
        }
    }
    return $colors;
}

function foregrounds () {
    return array_merge(greys(), colors());
}
