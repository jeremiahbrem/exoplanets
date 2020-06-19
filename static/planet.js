window.onload = function() {
  $('#exoplanet').css("transform", "scale(1)");
}

const radius = parseFloat($('#pl_rade').text());

comparePlanetSize(radius);

// converts B-V color index to rgb value
function getRGB(colorIndex) {
  const color = parseFloat(colorIndex);
  if (color >= 0.81) {
    const g = 255 - (color - 0.81) * 65.0558;
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

const rgb = getRGB($('#st_bmvj').text());
console.log(rgb)
addRGB(rgb);


function addRGB(rgb) {
    const values = "inset 0 0 5px white, inset 0 0 15px white, inset 0 0 60px white, 0 0 8px white, " +
        `0 0 30px white, 0 0 60px white, 0 0 60px 30px ${rgb}, 0 0 120px 60px ${rgb}, 0 0 240px 120px ${rgb}`
    
        $('#sun-glow').css("background-color", `${rgb}`)         
        document.getElementById("sun-glow").style.boxShadow = values;
}  


function comparePlanetSize(radius) {
    let exoRadius;
    let earthRadius;
    if (radius >= 6) {
      $('#exo').css({
            "width": "300px",
            "top": "-100px"
            });
      exoRadius = $('#exo').css("width").slice(0,-2);
      earthRadius = parseFloat(exoRadius) / parseFloat(radius)
      $('#earth').css("width", `${earthRadius}px`); 
    }       
    else {
      $('#earth').css("width", "50px");
      earthRadius = $('#earth').css("width").slice(0,-2);
      exoRadius = parseFloat(earthRadius) * parseFloat(radius);
      const top = exoRadius / 3;
      $('#exo').css({
          "width": `${exoRadius}px`,
          "top": `-${top}px`
          })
    }          
      
    
}