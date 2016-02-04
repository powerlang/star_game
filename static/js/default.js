(function ( $ ) {
    jQuery(document).ready(function() {

			
				$(".radioSex label").on("click",function(){
					$(this).addClass("on").siblings().removeClass("on");
				})
				
				
				var setIntervalId=window.setInterval(slideNews, 4500);   
				

				function slideNews(){
					$(".otherList li").css({marginTop: 0});
					var $firstNews = $(".otherList li").eq(0);
 					var moveH = -1*$firstNews.innerHeight();
					

					$firstNews.animate({
						marginTop: moveH
					}, 800, function() {
							$(".otherList ul").append($firstNews);
					});

				}





			$('.btnShare').click(function(){
				
				$(".shareMask").show();	
			});

    });
}( jQuery ));

