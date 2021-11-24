function setSearchTerm(){
						let temp = document.getElementById("searchBar").value;
						sessionStorage.setItem("searchItem",temp )
						location.reload();
						return;
}
// external js: flickity.pkgd.js