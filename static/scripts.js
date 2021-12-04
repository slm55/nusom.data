    function myFunction() {
        var x = document.getElementById("myNavbar");
        if (x.className === "navbar") {
          x.className += " responsive";
        } else {
          x.className = "navbar";
        }
      }

    $(document).ready(function() {

        $(".edt-btn").click(function(){
            $(".edt-btn").hide();
            $(".sbt-btn").show();
            $('.my-form input[type=text]').removeAttr('disabled');
            $('.my-form').attr('method', 'POST');
            $('.my-form').attr("action", "/edit");
        });

        $('.my-form input[type=text]').attr('disabled','disabled');
        $('.my-form input[type=submit]').hide();

        var dr = document.getElementById('doctor');
        if (dr) {
        dr.addEventListener('change', function(){
            var pos = document.getElementsByClassName('pos')[0];
            pos.innerHTML = '<div class="form-group  required"><label class="control-label" for="degree">Degree</label> <input class="form-control" id="degree" name="degree" required="" type="text" value=""></div>';
        }); }

        var ps = document.getElementById('ps');
        if (ps) {
        ps.addEventListener('change', function(){
            var pos = document.getElementsByClassName('pos')[0];
            pos.innerHTML = '<div class="form-group  required"><label class="control-label" for="department">Department</label> <input class="form-control" id="department" name="department" required="" type="text" value=""></div>';
        }); }
    });