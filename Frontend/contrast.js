const fs = require('fs');

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

function luminance(r, g, b) {
  var a = [r, g, b].map(function (v) {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
}

function contrast(hex1, hex2) {
  const rgb1 = hexToRgb(hex1);
  const rgb2 = hexToRgb(hex2);
  if (!rgb1 || !rgb2) return -1;
  const lum1 = luminance(rgb1.r, rgb1.g, rgb1.b);
  const lum2 = luminance(rgb2.r, rgb2.g, rgb2.b);
  const brightest = Math.max(lum1, lum2);
  const darkest = Math.min(lum1, lum2);
  return (brightest + 0.05) / (darkest + 0.05);
}

const colors = {
  ink: '#f0ede8',
  paper: '#0f0f0f',
  panel: '#1a1a1a',
  panelInput: '#212121',
  panelCard: '#1e1e1e',
  line: '#2a2a2a',
  muted: '#8a8680',
  amber: '#e8a838',
  amberDark: '#c47a1e',
  amberLight: '#f4d07a',
  moss: '#2fd48f',
  mossDark: '#123d2c',
  mossLight: '#6be8b4',
  clay: '#e05c3a',
  clayText: '#f07050',
  gold: '#f4c452',
  goldDark: '#c98f1f',
  violet: '#6e6a7a',
  violetLight: '#9896a4'
};

console.log("Checking contrast ratios...");
console.log("Text (ink) on paper:", contrast(colors.ink, colors.paper).toFixed(2));
console.log("Text (ink) on panel:", contrast(colors.ink, colors.panel).toFixed(2));
console.log("Text (muted) on panel:", contrast(colors.muted, colors.panel).toFixed(2));
console.log("Text (muted) on paper:", contrast(colors.muted, colors.paper).toFixed(2));
console.log("Text (amber) on panel:", contrast(colors.amber, colors.panel).toFixed(2));
console.log("Text (moss) on panel:", contrast(colors.moss, colors.panel).toFixed(2));
console.log("Text (clayText) on panel:", contrast(colors.clayText, colors.panel).toFixed(2));
console.log("Text (clay) on panel:", contrast(colors.clay, colors.panel).toFixed(2));
