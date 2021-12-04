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
            pos.innerHTML = '<div class="form-group  required"><label for="country">Degree</label><select id="degree" name="degree"><option value="MBBS">MBBS</option><option value="MD">MD</option><option value="PhD">PhD</option></select></div>';
        }); }

        var ps = document.getElementById('ps');
        if (ps) {
        ps.addEventListener('change', function(){
            var pos = document.getElementsByClassName('pos')[0];
            pos.innerHTML = '<div class="form-group  required"><label for="dept">Department</label><select id="dept" name="dept"><option value="Department of Molecular Medicine">Department of Molecular Medicine</option><option value="Department of Pharmacology">Department of Pharmacology</option><option value="Department of Public Health">Department of Public Health</option></select></div>';
        }); }
    });