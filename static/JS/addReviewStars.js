document.getElementById("star1").addEventListener("moveseover", unhoverStar, 1);
document.getElementById("star1").addEventListener("mouseout", hoverStar, 1);

document.getElementById("star2").addEventListener("moveseover", unhoverStar, 2);
document.getElementById("star2").addEventListener("mouseout", hoverStar, 2);

document.getElementById("star3").addEventListener("moveseover", unhoverStar, 3);
document.getElementById("star3").addEventListener("mouseout", hoverStar, 3);

document.getElementById("star4").addEventListener("moveseover", unhoverStar, 4);
document.getElementById("star4").addEventListener("mouseout", hoverStar, 4);

document.getElementById("star5").addEventListener("moveseover", unhoverStar, 5);
document.getElementById("star5").addEventListener("mouseout", hoverStar, 5);
function hoverStar(num){
for(let i  = 1; i <=num ; i++){

    document.getElementById("star"+i).style["color"] = "orange";
    console.log("star"+i);
}
}
function unhoverStar(num){
    for(let i  = 1; i <=num ; i++){
       
        document.getElementById("star"+i).style["color"] = "black";
    }
}