

    function getTimes() {
      var times = [];
      $.each($("input[name='time']:checked"), function(){            
                times.push($(this).val());
            });
      return times;
      //alert("You selected: " + times.join(", "));
    }

    function clearAllTimes() {
      $.each($("input[name='time']").prop("checked", false));
    }

    function selectAllTimes() {
      $.each($("input[name='time']").prop("checked", true));
    }

    function getCoins() {
      var coins = [];
      $.each($("input[name='coin']:checked"), function(){            
                coins.push($(this).val());
            });
      return coins;
      //alert("You selected: " + coins.join(", "));
    }

    function clearAllCoins() {
      $.each($("input[name='coin']").prop("checked", false));
    }

    function selectAllCoins() {
      $.each($("input[name='coin']").prop("checked", true));
    }


  $(document).ready(function() {

  $('form').on('submit', function(event) {
    var listCoins = getCoins();
    var listTimes = getTimes();
    alert("You selected: " + listCoins.join(", "));
    alert("You selected: " + listTimes.join(", "));
    $.ajax({
      data : {
        mycoins : listCoins,
        mytimes : listTimes
      },
      type : 'POST',
      url : '/process'
    })
    .done(function(data) {

      if (data.error) {
        $('#errorAlert').text(data.error).show();
        $('#successAlert').hide();
      }
      else {
        $('#successAlert').text(data.coins.join(", ")).show();
        $('#errorAlert').hide();
      }

    });

    event.preventDefault();

  });

});
