////odoo.define('patient_patient.custom', function (require) {
////"use strict";
////var core = require('web.core');
////var Model = require('web.Model')
////var KanbanRecord = require('web_kanban.Record');
////var patient_patient = new Model('patient.patient')
//////     patient_patient.call('my_function')
////
////var model  = patient_patient.call('my_function').then(function(){
////    console.log(11111);
////   // alert("133333333333333");
////    return "result";
////});
////
////
////KanbanRecord.include({
////    events: _.defaults({
////        'click .patient_click': 'patient_click_target_click',
////    }, KanbanRecord.prototype.events),
////
////    patient_click_target_click: function(ev) {
////        ev.preventDefault();
//////        this.$target_input = $('<input>');
//////        this.$('.o_kanban_primary_bottom').html(this.$target_input);
//////        this.$('.o_kanban_primary_bottom').prepend(_t("Set an invoicing target: "));
//////        this.$target_input.focus();
////        var self = this;
////    },
////});
////
//////function clickMe(){
//////    alert("it works!!");
//////};
////
////});
//
//
//odoo.define('website_variants.website_variant', function (require) {
// "use strict";
//$(document).ready(function() {
// $('#kha').click(function (e){
//alert('ssssssssssssssssssssssssss');
//// var x = document.getElementById("hidden_box");
////            if (x.style.display === "none") {
////                x.style.display = "block";
////                    } else {
////                        x.style.display = "none";
////                    }
//});
//
//});
//
//});

odoo.define('patient_patient.custom', function (require) {
"use strict";
console.log(self);

self.$('.kha').click(function() {
                    alert('hello1111111111');

                    var printer = window.open('left=0', 'top=0', 'width=300,height=300');
                    printer.document.open("text/html");
                    printer.document.write(document.getElementById('advancePrintArea').innerHTML);
                    printer.print();
                    printer.document.close();
                    printer.window.close();

                    });


});

