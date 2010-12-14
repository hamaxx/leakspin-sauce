var tagsCache;
var hash = "empty";
var title = "leakspin: sauce - ";

$(document).ready(function() {
	setInterval(function() {
		var cable = document.location.hash.substring(2);
		load(cable);
	}, 50);
	
	$("#gotoCable").submit(function(e) {
		e.preventDefault();
		load($("#cable").val());
	});
	
	$("#header a").click(function() {
		load("");
	});
	
	$.ajaxSetup({
		error:function(e, x){
			$("#content").html("<h2 id=\"error\">Sorry, no content to display.</h2>");
			$("#content").css("width", "900px");
			$(".left").css("display", "none");
		}
	});
});

function load(cable) {
	if (hash == cable) return;
	
	$("#cable").val(cable);
	document.location.hash = "!" + cable;
	hash = cable;
	
	if (cable.length > 0 && cable.match(/[0-9]{2}[A-Z]+[0-9]+/)) {
		$(".left").css("display", "block");
		$("#content").css("width", "600px");
		loadCable(cable);
	} else {
		$(".left").css("display", "none");
		$("#content").css("width", "900px");
		loadTags(cable);
	}
	
	if (cable.length <= 0) {
		$("title").html(title + "home");
	} else {
		$("title").html(title + cable);
	}
}

function loadTags(tag) {
	$("#content").html("<div class='cell cell0'></div><div class='cell cell1'></div><div class='cell cell2'></div>");
	var re = new RegExp(tag,"i");

	initTags(function(data) {
		var alltags = [];
		
		for (var i in data) {
			if ((!tag && data[i].len > 10) || (tag.length > 0 && data[i].tag.match(re))) {
				alltags.push(data[i]);
			}
		}
		
		if (alltags.length == 0) {
			$("#content").html("<h2 id=\"error\">Sorry, no content to display.</h2>");
		}
		
		var c = 0;
		var columnSize = alltags.length / 3;
		for (var i in alltags) {
			var tagObjWrap = $("<div></div>");
			var tagli = $("<a href=\"#!" + alltags[i].tag + "\" class='tagli'><span>"+alltags[i].tag + "</span> (" + alltags[i].len +")</a>");
			tagObjWrap.append(tagli);
			
			
			var col = Math.min(Math.floor(c / columnSize), 2);
			$("#content").find(".cell" + col).append(tagObjWrap);
			
			tagli.click(function() {
				if ($(this).parent().find(".tagsSublist").length > 0) {
					$(this).parent().find(".tagsSublist").remove();
				} else {
					articlesForTag($(this));
				}
				return false;
			});
			if (tagObjWrap.height() > 20) {
				c++;
				columnSize += 1.0/3;
			}
			c++;	
		}
		
	});
}

function initTags(callback) {
	if (tagsCache) {
		callback(tagsCache);
	} else {
		$.get("tags/list.txt", function(data) {
			data = JSON.parse(data);
			tagsCache = data;
			callback(data);
		});
	}
}

function loadCable(cable) {
	$("#relatedCables").html("");
	$("#articles").html("");
	$("#tags").html("");
	
	$.get("filtered/" + cable + ".txt", function(data) {
		data = filterMeta(data);	
		zemify(cable, data);
	});
	relatedCables(cable);
}

function filterMeta(data) {
	var brake = data.search(new RegExp("introduction", "i"));
	if (brake < 0) brake = data.search(new RegExp("Summary", "i"));
	if (brake < 0) brake = data.search(new RegExp("1\\. \\(", "i"));
	if (brake < 0) brake = data.search(new RegExp("Classified By", "i"));
	
	var meta = data.substring(0, brake);
	var body = data.substring(brake);
	
	var metaHead = "<a id=\"metaHead\" href=\"#expand_meta\">Expand Meta Data</a>";
	var metaBodyWrap = "<div id=\"metaBody\">" + meta + "</div>";
	
	var subject = "";
	var subjectFrom = meta.search(new RegExp("subject", "i"));
	var subjectTo = -1;
	if (subjectFrom > 0) {
		subjectFrom = meta.indexOf(" ", subjectFrom);
		if (subjectFrom > 0) {
			subjectTo = meta.indexOf("\n", subjectFrom);
			if (subjectTo > 0) {
				subject = "<h2>" + meta.substring(subjectFrom, subjectTo) + "</h2>";
			}
		}
	}
	
	return subject + metaHead + metaBodyWrap + body + "\n\n";
}

function zemify(cable, text) {
	$.get("zemanta/" + cable + ".txt", function(data) {
		data = JSON.parse(data);
		markup(data, text);
		image(data);
		tags(data);
		articles(data);
	});
}

function relatedCables(cable) {
	$.get("related/" + cable + ".txt", function(data) {
		data = JSON.parse(data);
		for (var i in data) {
			if (i > 15) break;
			
			var link = $("<a href=\"#!" + data[i].cable + "\" class=\"tag tagLink\" cable=\""+data[i].cable+"\">" + humanCable(data[i].cable) + "</a>");
			$("#relatedCables").append(link);
			link.click(function() {
				load($(this).attr("cable"));
				return false;
			});
		}
	});
}

function tags(data) {
	var tags = data.keywords;
	for (var i in tags) {
		var tagObjWrap = $("<div></div>");
		var tagObj = $("<a href=\"#!" + tags[i].name + "\"  class=\"tag tagLink\"><span>" + tags[i].name + "</span></a>");
		tagObjWrap.append(tagObj);
		$("#tags").append(tagObjWrap);
		
		tagObj.click(function() {
			if ($(this).parent().find(".tagsSublist").length > 0) {
				$(this).parent().find(".tagsSublist").remove();
			} else {
				articlesForTag($(this));
			}
			return false;
		});
	}
}

function articlesForTag(obj) {
	var fn = obj.find("span").text().replace(/[\/\?\*\:\|"<>\\]/g, "_");
	$.get("tags/" + fn + ".txt", function(data) {
		data = JSON.parse(data);
		var links = $("<div class=\"tagsSublist\"></div>");
		var allData = [];
		for (var i in data) {
			if ($("#cable").val() != data[i].cable) {
				allData[i] = [humanCable(data[i].cable), data[i].cable];
			}
		}
		
		allData.sort(function(a, b) {return a[0] < b[0]});
		
		for (var i in allData) {
			var link = $("<a href=\"#!" + allData[i][1] + "\" cable=\""+ allData[i][1] +"\">" + allData[i][0] + "</a>");
			links.append(link);
			link.click(function() {
				load($(this).attr("cable"));
				return false;
			});		
		}
		
		obj.parent().append(links);
	});
}

function articles(data) {
	var articles = data.articles;
	for (var i in articles) {
		$("#articles").append("<a target=\"blank_\" href=\"" + articles[i].url + "\" class=\"tag\">" + articles[i].title + "</a>");
	}
}

function image(data) {
	var images = data.images;
	if (images.length <= 0) return;
	
	var image;
	for (var i in images) {
		if (images[i].url_m_w * images[i].url_m_h > 200 * 200) {
			image = images[i];
			break;
		}
	}
	
	if (image != undefined) {
		var img = $('<img src="'+image.url_m+'" alt="'+image.description+'" title="'+image.description+'" / >');
		$("#content").prepend($('<a target="_blank" href="'+image.url_l+'"></a>').append(img));
		img.error(function(e, x) {
			$(this).remove();
		});
	}
}

function markup(data, text) {
	var links = data.markup.links;
	if (links.length <= 0) return;
	
	for (var i in links) {
		var anchor = links[i].anchor;
		
		var target = links[i].target[0];
		if (target.type != "wikipedia") {
			for (var j in links[i].target) {
				if (links[i].target[j].type == "wikipedia") {
					target = links[i].target[j];
				}
			}
		}
		var reg = new RegExp(anchor, "g");
		text = text.replace(reg, "<a target=\"_blank\" href=\"" + target.url + "\" title=\""+target.title+"\">" + anchor + "</a>");
	}
	
	text = text.replace(/\n/g, "<br / >");
	$("#content").html(text);
	
	$("#metaHead").click(function() {
		if ($("#metaBody").css("display") == "none") {
			$("#metaBody").css("display", "block");
			$("#metaHead").html("Hide Meta Data");
		} else {
			$("#metaBody").css("display", "none");
			$("#metaHead").html("Expand Meta Data");
		}
		return false;
	});
}

function humanCable(cable) {
	var p = cable.match(/([0-9]{2})([A-Z]+)([0-9]+)/);
	return (parseInt(p[1]) < 50 ? "20" : 19) + p[1] + ": " + p[2].substring(0, 1) + p[2].toLowerCase().substring(1) + " " + p[3];
}
