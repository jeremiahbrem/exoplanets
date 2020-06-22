// zoom in to planet and star *** COMMENT THIS OUT FOR JASMINE TESTS ***
window.onload = function() {
  $('.exoplanet-zoom').css("transform", "scale(1)");
}

const planetRadius = parseFloat($('#pl_rade').text());
const starRadius = parseFloat($('#st_rad').text());
const planetMass = parseFloat($('#pl_masse').text());
const habitable = $('#habitable').text();
const orbit = parseFloat($('#pl_orbsmax').text());

// adds image for exoplanet
const pic = getPlanetPic(planetMass, habitable, orbit, planetRadius);
$('#exo').attr("src", pic);
$('#big-exo-image').attr("src", pic);

// add widths to planet images
if (planetRadius) {
  $('#pl-comparisons').show()
  const planetWidths = comparePlanetSize(planetRadius);
  $('#earth').css("width", `${planetWidths.earthWidth}px`)
  $('#exo').css({
          "width": `${planetWidths.exoWidth}px`,
          "top": "10px"
          })
}

// get star comparison scale sizes
const starScales = compareStarSize(starRadius);

// add scale sizes to screen
$('#exo-sun-small').css("transform", `scale(${starScales.exoScale})`);
$('#sun').css("transform", `scale(${starScales.sunScale})`);


// converts B-V color index to rgb value
function getRGBFromBV(colorIndex) {
  const color = parseFloat(colorIndex);
  if (color >= 0.81) {
    const g = 255 - (color - 0.81) * 150;
    return `rgb(255,${g},0)`
  }    
  else if (color < 0.81 && color >0.43) {
    const b = 255-(color - 0.44) * 705.5556;
    return `rgb(255,255,${b})`
  }
  else if (color <= 0.43) {
    const r = 254 - (0.43 - color) * 223.0769;
    return `rgb(${r},${r},255)`
  }
}

// returns a planet pic depending on habitable zone, mass, orbit, radius
function getPlanetPic(mass, habitability, orbit, radius) {
  if (habitability == "Habitable") {
    return "/static/images/exoplanet-hab.png"
  }
  else if ((habitability == "Unknown") && (!mass || mass <= 10)) {
    return "/static/images/exoplanet-hab.png"
  }
  else if (((habitability == "Too cold") && orbit > 20) && (!mass || (mass > 10 && mass < 50))) {
    return "/static/images/cold-giant.jpg"
  }
  else if ((habitability == "Too cold") && (!mass || mass <= 10) && (!radius || radius < 5) && orbit < 20) {
    return "/static/images/cold-planet.jpg"
  }
  else if (habitability == "Too hot" && (!mass || mass <= 10)) {
    return "/static/images/hot-planet.jpg"
  }
  else if (habitability == "Too hot" || (mass > 10)) {
    return "/static/images/gas-giant.jpg"
  }
  else {
    return "/static/images/gas-giant.jpg"
  }
}

// converts spectral type to B-V if no B-V given
function getBVFromSpectral(spectralType) {
  const firstChar = spectralType[0];
  const secondChar = parseInt(spectralType[1]);
  if (firstChar == "B") {
    if (secondChar > 0) {
      return -0.3 + secondChar * .027
    }
    else {
      return -0.3
    }
  }
  if (firstChar == "A") {
    if (secondChar > 0) {
      return -0.02 + secondChar * .032
    }
    else {
      return -0.02
    }
  }
  if (firstChar == "F") {
    if (secondChar > 0) {
      return 0.3 + secondChar * .028
    }
    else {
      return 0.3
    }
  }
  if (firstChar == "G") {
    if (secondChar > 0) {
      return 0.58 + secondChar * .023
    }
    else {
      return 0.58
    }
  }
  if (firstChar == "K") {
    if (secondChar > 0) {
      return 0.81 + secondChar * .08
    }
    else {
      return 0.81
    }
  }
  if (firstChar == "M") {
    if (secondChar > 0) {
      return 1.4 + secondChar * .185
    }
    else {
      return 1.4
    }
  }
}

// return B-V index calculated from star surface temp
function getBVFromTemp(temp) {
  const num1 = .27 / 20210;
  const num2 = .32 / 2490;
  const num3 = .28 / 1360;
  const num4 = .23 / 790;
  const num5 = .59 / 1310;
  const num6 = 1 / 840;

  if (temp > 9790) {
    return -0.3 + (30000 - temp) * num1;
  }
  else if (temp <= 9790 && temp > 7300) {
    return -0.02 + (9790 - temp) * num2;
  }
  else if (temp <= 7300 && temp > 5940) {
    return 0.3 + (7300 - temp) * num3;
  }
  else if (temp <= 5940 && temp > 5150) {
    return 0.58 + (5940 - temp) * num4;
  }
  else if (temp <= 5150 && temp > 3840) {
    return 0.81 + (5150 - temp) * num5;
  }
  else if (temp <= 3840) {
    return 1.4 + (3840 - temp) * num6;
  }
}

// brown dwarf star
if (parseInt($('#st_teff').text()) < 1000) {
  addRGB("rgb(43,24,2)")
}
// use B-V index for star color
else if ($('#st_bmvj').text() != "None") {
  const rgb = getRGBFromBV($('#st_bmvj').text());
  addRGB(rgb);
}
// use surfac temp for star color
else if ($('#st_teff').text() != "None") {
  const bv = getBVFromTemp($('#st_teff').text());
  const rgb = getRGBFromBV(bv);
  addRGB(rgb);
}
// use spectral type for star color
else if ($('#st_spstr').text() != "None") {
  const bv = getBVFromSpectral($('#st_spstr').text());
  const rgb = getRGBFromBV(bv);
  addRGB(rgb);
}

// adds color and shading to star
function addRGB(rgb) {
  const values = "inset 0 0 5px white, inset 0 0 15px white, inset 0 0 60px white, 0 0 8px white, " +
        `0 0 30px white, 0 0 60px white, 0 0 60px 30px ${rgb}, 0 0 120px 60px ${rgb}, 0 0 240px 120px ${rgb}`
    
  $('#exo-sun-glow, #exo-sun-small').css("background-color", `${rgb}`)         
  document.getElementById("exo-sun-glow").style.boxShadow = values;
  document.getElementById("exo-sun-small").style.boxShadow = values;
}  

// returns scale sizes for stars
function compareStarSize(starRadius) {
  let exoRadius;
  let exoScale;
  let sunRadius;
  let sunScale;
  if (starRadius > 1) {
    exoScale = 0.5;
    $('#exo-sun-small').css("transform", "scale(0.5)");
    sunScale = 1 / (starRadius * 2) 
    $('#sun').css("transform", `scale(${sunRadius})`);
  }
  else {
    sunScale = 0.5;
    exoScale = starRadius / 2;
  }
  return {"sunScale": sunScale, "exoScale": exoScale}
}

// return image widths for planets
function comparePlanetSize(planetRadius) {
  let exoRadius;
  let earthRadius;
  let exoWidth;
  let earthWidth;
  if (planetRadius >= 6) {
    exoWidth = 300;
    earthWidth = exoWidth / parseFloat(planetRadius);
  }    
  else {
    earthWidth = 50;
    exoWidth =  earthWidth * parseFloat(planetRadius);
  }          
  return {"earthWidth": earthWidth, "exoWidth": exoWidth}
}