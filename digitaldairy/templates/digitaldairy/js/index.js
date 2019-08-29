if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/service-worker.js', {
            scope: '/static/',
        }).then((registration) => {
            console.log('[Service Worker] registered.', registration);
            // return registration.pushManager.getSubscription().then(async function (subscription) {
            //     //registration part
            //     if (subscription) {
            //         return subscription;
            //     } else {
            //         // const response = await fetch('./vapidPublicKey');
            //         // const vapidPublicKey = await response.text();
            //         // const convertedVapidKey = urlBase64ToUint8Array(vapidPublicKey);
            //         // return registration.pushManager.subscribe({
            //         //     userVisibleOnly: true,
            //         //     applicationServerKey: convertedVapidKey
            //         // });
            //     }
            // });
        }, /*catch*/(error) => {
            console.log('[Service Worker] registration failed:', error);
        }).then((subscription) => {
            console.log('[Service Worker] subscription ' + subscription)
            //subscription part
            //send subscription details as JSON to the server using fetch
            // fetch('./register', {
            //     method: 'post',
            //     headers: {
            //         'Content-type': 'application/json'
            //     },
            //     body: JSON.stringify({ subscription: subscription })
            // });
        });
        //request to show notifications when the user requests it by creating /// a button
        var button = document.getElementById('notifications-button');
        if (button) {
            button.addEventListener('click', function (event) {
                Notification.requestPermission().then((result) => {
                    if (result === 'granted') {
                        randomNotification();
                    }
                });
            });
        }
        function randomNotification() {
            var randomItem = Math.floor(Math.random() * 1000);
            var notifTitle = 'Notification Title';
            var notifBody = 'Created by Brian Muciri';
            var notifImg = ''
            var options = {
                body: notifBody,
                icon: notifImg,
            }
            var notif = new Notification(notifTitle, options);
            setTimeout(randomNotification, 30000);
        }
    });
}
else {
    console.log('Service workers are not supported.');
}

var postUrl = 'https://digitaldairy.herokuapp.com';
//var postUrl = 'http://127.0.0.1:8000';
var option = document.createElement('option');
function clearTextAndNumberInputFields(modal) {
    modal.find('input[type=number]').val(0);
    modal.find('input[type=text]').val('');
}
var myStorage = window.sessionStorage;
function getDate(date) {
    // add year to date string
    var date_string = new String(date.getUTCFullYear());
    // add month to date string
    //    date_string = date_string.concat(date.getUTCMonth() + 1 < 10 ? '-0'+(date.getUTCMonth() + 1) :  '-'+(date.getUTCMonth() +1));
    date_string = date_string.concat('-0' + 5);
    // add current date to date string
    //	date_string = date_string.concat(date.getUTCDate() < 10 ? '-0'+date.getUTCDate() :'-'+date.getUTCDate());
    date_string = date_string.concat('-' + 16);
    return date_string;
}
var current_date_string = getDate(new Date());
$('input[type=date]').toArray().forEach(function (dateInputField) {
    if (dateInputField.value == "") {
        dateInputField.value = current_date_string;
    }
});
$('input[type=number]').toArray().forEach(function (numberInputField) {
    if (numberInputField.value === '') {
        numberInputField.value = '';
    }
});
$('input[name=year]').toArray().forEach(function (yearInputField) {
    if (yearInputField.value == 0) {
        yearInputField.value = new Date().getUTCFullYear();
    }
});
$('#milkInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var cow_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'editMilkProductionBtn') {
        modal.find('.modal-title').text("Edit Milk Production Record")
        var milk_p = JSON.parse(myStorage.getItem('milk_p_' + cow_id))
        var milk_p_id_input = modal.find('input[name=milk_production_id]')
        if (milk_p_id_input.length == 1) {
            milk_p_id_input.val(milk_p.id)
        }
        else {
            milk_p_id_input = "<input id='milk_production_id' type='hidden' class='form-control' name='milk_production_id'>";
            modal.find('#milk_date').after(milk_p_id_input)
            milk_p_id_input = modal.find('input[name=milk_production_id]')
            milk_p_id_input.val(milk_p.id)
        }
        modal.find('#milk_date').val(milk_p.milk_date)
        modal.find('#am_quantity').val(milk_p.am_quantity)
        modal.find('#noon_quantity').val(milk_p.noon_quantity)
        modal.find('#pm_quantity').val(milk_p.pm_quantity)
        modal.find("#cow_id").val(milk_p.cow_id).trigger('change');
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Milk Production Record")
        modal.find('input[name=milk_production_id]').remove()
    }
})
$('#targetInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var cow_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'editMilkProductionTargetBtn') {
        modal.find('.modal-title').text("Edit Milk Production Target Record")
        var milk_p_target = JSON.parse(myStorage.getItem('milk_p_target_' + cow_id))
        modal.find('#milk_production_target').val(milk_p_target.target_quantity)
        modal.find("#cow_id").val(milk_p_target.cow_id).trigger('change');
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Milk Production Target Record")
    }
})
$('#consumerInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var consumer_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'editConsumerBtn') {
        modal.find('.modal-title').text("Edit Consumer Details")
        var consumer = JSON.parse(myStorage.getItem('consumer_' + consumer_id))
        var consumer_id_input = modal.find('input[name=consumer_id]')
        if (consumer_id_input.length == 1) {
            consumer_id_input.val(consumer.id)
        }
        else {
            consumer_id_input = "<input id='consumer_id' type='hidden' class='form-control' name='consumer_id'>";
            modal.find('#consumer_name').before(consumer_id_input)
            consumer_id_input = modal.find('input[name=consumer_id]')
            consumer_id_input[0].value = consumer.id
        }
        modal.find('#consumer_name').val(consumer.consumer_name)
        modal.find('#consumer_contacts').val(consumer.consumer_contacts)
        modal.find('#consumer_location').val(consumer.consumer_location)
    }
    else {
        modal.find('input[name=consumer_id]').remove();
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Consumer Record")
    }
})
$('#clientInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var client_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'editClientBtn') {
        modal.find('.modal-title').text("Edit Client Details")
        var client = JSON.parse(myStorage.getItem('client_' + client_id))
        var client_id_input = modal.find('input[name=client_id]')
        if (client_id_input.length == 1) {
            client_id_input.val(client.id)
        }
        else {
            client_id_input = "<input id='client_id' type='hidden' class='form-control' name='client_id'>";
            modal.find('#client_name').before(client_id_input)
            client_id_input = modal.find('input[name=client_id]')
            client_id_input[0].value = client.id
        }
        modal.find('#client_name').val(client.client_name)
        modal.find('#client_contacts').val(client.client_contacts)
        modal.find('#client_location').val(client.client_location)
        modal.find('#client_unit_price').val(client.client_unit_price)
    }
    else {
        modal.find('input[name=client_id]').remove();
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Client Record")
    }
})
$('#milkSaleInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var milk_sale_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'milkSaleEditBtn') {
        modal.find('.modal-title').text("Edit Milk Sale Record")
        var milk_sale = JSON.parse(myStorage.getItem('milk_sale_' + milk_sale_id))
        var milk_sale_id_input = modal.find('input[name=milk_sale_id]')
        if (milk_sale_id_input.length == 1) {
            milk_sale_id_input.val(milk_sale.id)
        }
        else {
            milk_sale_id_input = "<input id='milk_sale_id' type='hidden' class='form-control' name='milk_sale_id'>";
            modal.find('#sale_date').before(milk_sale_id_input)
            milk_sale_id_input = modal.find('input[name=milk_sale_id]')
            milk_sale_id_input[0].value = milk_sale.id
        }
        modal.find('#client_id').val(milk_sale.client_id)
        modal.find('#sale_date').val(milk_sale.sale_date)
        modal.find('#sale_quantity').val(milk_sale.sale_quantity)
    }
    else {
        modal.find('input[name=milk_sale_id]').remove()
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Milk Sale Record")
    }
})
$('#milkPaymentsInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var milk_sale_payment_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'milkSalePaymentEditBtn') {
        modal.find('.modal-title').text("Edit Milk Sale Payment Record")
        var milk_payment = JSON.parse(myStorage.getItem('milk_sale_payment_' + milk_sale_payment_id))
        var milk_sale_payment_id_input = modal.find('input[name=milk_sale_payment_id]')
        if (milk_sale_payment_id_input.length == 1) {
            milk_sale_payment_id_input.val(milk_payment.id)
        }
        else {
            milk_sale_payment_id_input = "<input id='milk_sale_payment_id' type='hidden' class='form-control' name='milk_sale_payment_id'>";
            modal.find('#payment_date').before(milk_sale_payment_id_input)
            milk_sale_payment_id_input = modal.find('input[name=milk_sale_payment_id]')
            milk_sale_payment_id_input.val(milk_payment.id)
        }
        modal.find('#client_id').val(milk_payment.client_id)
        modal.find('#payment_date').val(milk_payment.date_of_payment)
        modal.find('#from_date').val(milk_payment.from_date)
        modal.find('#to_date').val(milk_payment.to_date)
        modal.find('#amount_paid').val(milk_payment.amount_paid)
    }
    else {
        modal.find('input[name=milk_sale_payment_id]').remove()
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Milk Sale Payment Record")
    }
})
$('#milkConsumptionInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var milk_consumption_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'milkConsumptionEditBtn') {
        modal.find('.modal-title').text("Edit Milk Consumption Details")
        var milk_consumption = JSON.parse(myStorage.getItem('milk_consumption_' + milk_consumption_id))
        var milk_consumption_id_input = modal.find('input[name=milk_consumption_id]')
        if (milk_consumption_id_input.length == 1) {
            milk_consumption_id_input.val(milk_consumption.id)
        }
        else {
            milk_consumption_id_input = "<input id='milk_consumption_id' type='hidden' class='form-control' name='milk_consumption_id'>";
            modal.find('#consumption_date').before(milk_consumption_id_input)
            milk_consumption_id_input = modal.find('input[name=milk_consumption_id]')
            milk_consumption_id_input.val(milk_consumption.id)
        }
        modal.find('#consumption_date').val(milk_consumption.consumption_date)
        modal.find('#consumer_id').val(milk_consumption.consumer_id)
        modal.find('#consumed_quantity').val(milk_consumption.consumption_quantity)
    }
    else {
        modal.find('input[name=milk_consumption_id]').remove();
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Consumption Record")
    }
})
$('#cowInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var cow_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'cowEditBtn') {
        modal.find('.modal-title').text("Edit Cow Details")
        var cow = JSON.parse(myStorage.getItem('cow_' + cow_id));
        modal.find('#cow_id').val(cow.cow_id)
        modal.find('#cow_name').val(cow.cow_name)
        modal.find('#grade').val(cow.cow_grade)
        modal.find('#breed').val(cow.cow_breed)
        modal.find('#color').val(cow.cow_color)
        modal.find('#lactations').val(cow.cow_lactations)
        modal.find('#date_of_birth').val(cow.cow_dob)
        if (cow.cow_sire == 'None') {
            cow.cow_sire = ''
        }
        if (cow.cow_dam == 'None') {
            cow.cow_dam = ''
        }
        modal.find('#sire_id').val(cow.cow_sire)
        modal.find('#dam').val(cow.cow_dam)
        modal.find('#category').val(cow.cow_category)
        modal.find('#birth_weight').val(cow.birth_weight)
        modal.find('#group').val(cow.cow_group)
        modal.find('#source').val(cow.cow_source)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Cow Record")
    }
})
$('#weightInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var weight_record_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'weightEditBtn') {
        modal.find('.modal-title').text("Edit Weight Record Details")
        var weight_record = JSON.parse(myStorage.getItem('weight_' + weight_record_id))
        var weight_id_input = modal.find('input[name=weight_id]')
        if (weight_id_input.length == 1) {
            weight_id_input.val(weight_record.id)
        }
        else {
            weight_id_input = "<input id='weight_id' type='hidden' class='form-control' name='weight_id'>";
            modal.find('#weight_date').before(weight_id_input)
            weight_id_input = modal.find('input[name=weight_id]')
            weight_id_input.val(weight_record.id)
        }
        modal.find('#weight_date').val(weight_record.weight_date)
        modal.find('#cow_id').val(weight_record.cow_id)
        modal.find('#animal_weight').val(weight_record.animal_weight)
        modal.find('#animal_height').val(weight_record.animal_height)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Weight Record")
        modal.find('input[name=weight_id]').remove()
    }
})
$('#cowSaleInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var cow_sale_record_name = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'cowSaleEditBtn') {
        modal.find('.modal-title').text("Edit Sale Record Details")
        var cow_sale_record = JSON.parse(myStorage.getItem('cow_sale_' + cow_sale_record_name))
        modal.find('#cow_id').val(cow_sale_record.cow_id)
        modal.find('#sale_date').val(cow_sale_record.sale_date)
        modal.find('#client_name').val(cow_sale_record.client_name)
        modal.find('#cow_value').val(cow_sale_record.cow_value)
        modal.find('#sale_remarks').val(cow_sale_record.sale_remarks)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('#cow_id').val('cow_id')
        modal.find('.modal-title').text("Add Sale Record")
    }
})
$('#treatmentInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var treatment_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'treatmentEditBtn') {
        modal.find('.modal-title').text("Edit Treatment Record Details")
        var treatment = JSON.parse(myStorage.getItem('treatment_' + treatment_id))
        modal.find('#cow_id').val(treatment.cow_id)
        var treatment_id_input = modal.find('input[name=treatment_id]')
        if (treatment_id_input.length == 1) {
            treatment_id_input.val(treatment.treatment_id)
        }
        else {
            treatment_id_input = "<input id='treatment_id' type='hidden' class='form-control' name='treatment_id'>";
            modal.find('#treatment_date').after(treatment_id_input)
            treatment_id_input = modal.find('input[name=treatment_id]')
            treatment_id_input.val(treatment.treatment_id)
        }
        modal.find('#treatment_date').val(treatment.treatment_date)
        modal.find('#disease').val(treatment.disease)
        modal.find('#diagnosis').val(treatment.diagnosis)
        modal.find('#treatment').val(treatment.treatment)
        modal.find('#treatment_cost').val(treatment.treatment_cost)
        modal.find('#vet_name').val(treatment.vet_name)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Treatment Record")
        modal.find('input[name=treatment_id]').remove()
        modal.find('#cow_id').val('cow_id')
    }
})
$('#dewormingInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var deworming_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'dewormingEditBtn') {
        modal.find('.modal-title').text("Edit Deworming Record Details")
        var deworming = JSON.parse(myStorage.getItem('deworming_' + deworming_id))
        modal.find('#cow_id').val(deworming.cow_id)
        deworming_id_input = modal.find('input[name=deworming_id]')
        if (deworming_id_input.length == 1) {
            deworming_id_input.val(deworming.deworming_id)
        }
        else {
            var deworming_id_input = "<input id='deworming_id' type='hidden' class='form-control' name='deworming_id'>";
            modal.find('#deworming_date').after(deworming_id_input)
            deworming_id_input = modal.find('input[name=deworming_id]')
            deworming_id_input.val(deworming.deworming_id)
        }
        modal.find('#deworming_date').val(deworming.deworming_date)
        modal.find('#dewormer').val(deworming.dewormer)
        modal.find('#next_deworming_date').val(deworming.next_deworming_date)
        modal.find('#deworming_cost').val(deworming.deworming_cost)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Deworming Record")
        modal.find('#cow_id').val('cow_id')
        modal.find('input[name=deworming_id]').remove()
    }
})
$('#vaccineInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var vaccination_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'vaccinationEditBtn') {
        modal.find('.modal-title').text("Edit Vaccination Record Details")

        var vaccination = JSON.parse(myStorage.getItem('vaccination_' + vaccination_id))
        modal.find('#cow_id').val(vaccination.cow_id)
        var vaccination_id_input = modal.find('input[name=vaccination_id]')
        if (vaccination_id_input.length == 1) {
            vaccination_id_input.val(vaccination.vaccination_id)
        }
        else {
            vaccination_id_input = "<input id='vaccination_id' type='hidden' class='form-control' name='vaccination_id'>";
            modal.find('#vaccination_date').before(vaccination_id_input)
            vaccination_id_input = modal.find('input[name=vaccination_id]')
            vaccination_id_input.val(vaccination.vaccination_id)
        }
        modal.find('#vaccination_date').val(vaccination.vaccination_date)
        modal.find('#vaccine').val(vaccination.vaccine)
        modal.find('#next_vaccination_date').val(vaccination.next_vaccination_date)
        modal.find('#vaccination_cost').val(vaccination.vaccination_cost)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Vaccination Record")
        modal.find('input[name=vaccination_id]').remove()
        modal.find('#cow_id').val('cow_id')
    }
})
$('#calfFeedingInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var calf_feeding_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'calfManagementEditBtn') {
        modal.find('.modal-title').text("Edit Calf Feeding Record")
        var calf_feeding = JSON.parse(myStorage.getItem('calf_feeding_' + calf_feeding_id))
        modal.find('#calf_id').val(calf_feeding.cow_id)
        var calf_feeding_id_input = modal.find('input[name=calf_feeding_id]')
        if (calf_feeding_id_input.length == 1) {
            calf_feeding_id_input.val(calf_feeding.id)
        }
        else {
            calf_feeding_id_input = "<input id='calf_feeding_id' class='form-control' type='hidden' name='calf_feeding_id' required>";
            modal.find('#feeding_date').before(calf_feeding_id_input)
            calf_feeding_id_input = modal.find('input[name=calf_feeding_id]')
            calf_feeding_id_input.val(calf_feeding.id)
        }
        modal.find('#feeding_date').val(calf_feeding.feeding_date)
        modal.find('#milk_quantity').val(calf_feeding.milk_quantity)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Calf Feeding Record")
        modal.find('input[name=calf_feeding_id]').remove()
        modal.find('#calf_id').val('cow_id')
    }
})
$('#animalDeathInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var death_cow_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'cowDeathEditBtn') {
        modal.find('.modal-title').text("Edit Death Record")
        var death_record = JSON.parse(myStorage.getItem('death_' + death_cow_id))
        modal.find('#cow_id').val(death_record.cow_id)
        modal.find('#death_date').val(death_record.death_date)
        modal.find('#death_cause').val(death_record.death_cause)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Cow Death Record")
        modal.find('#cow_id').val('cow_id')
    }
})
$('#animalAutopsyInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var death_cow_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'autopsyEditBtn') {
        modal.find('.modal-title').text("Edit Autopsy Record")
        var death_record = JSON.parse(myStorage.getItem('death_' + death_cow_id))
        option.setAttribute('value', death_record.cow_id);
        option.innerText = death_record.cow_id
        if (modal.find('select#death_record_id').val(death_record.cow_id)[0].selectedIndex == -1) {
            modal.find('select#death_record_id')[0].add(option)
            modal.find('select#death_record_id').val(death_record.cow_id)
        }
        modal.find('#autopsy_date').val(death_record.autopsy_date)
        modal.find('#autopsy_cost').val(death_record.autopsy_cost)
        modal.find('#autopsy_results').val(death_record.autopsy_results)
        modal.find('#vet_name').val(death_record.vet_name)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text(" Add Autopsy Record")
        modal.find('#cow_id').val('cow_id')
    }
})
$('#employeesInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var employee_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'employeeEditBtn') {
        modal.find('.modal-title').text("Edit Employee Details")
        var employee_record = JSON.parse(myStorage.getItem('employee_' + employee_id))
        modal.find('#employee_name').val(employee_record.name)
        modal.find('#employee_id').val(employee_record.id)
        modal.find('#employee_contacts').val(employee_record.contacts)
        modal.find('#date_hired').val(employee_record.date_hired)
        modal.find('#department').val(employee_record.department)
        modal.find('#designation').val(employee_record.designation)
        modal.find('#salary').val(employee_record.salary)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text(" Add Employee Record")
    }
})
$('#semenInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var semen_catalog_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'semenCatalogEditBtn') {
        modal.find('.modal-title').text("Edit Semen Catalog Details")
        var semen_catalog = JSON.parse(myStorage.getItem('semen_catalog_' + semen_catalog_id))
        modal.find('#bull_name').val(semen_catalog.bull_name)
        modal.find('#bull_code').val(semen_catalog.bull_code)
        modal.find('#bull_breed').val(semen_catalog.bull_breed)
        modal.find('#num_of_straws').val(semen_catalog.num_of_straws)
        modal.find('#cost_per_straw').val(semen_catalog.cost_per_straw)
        modal.find('#company_name').val(semen_catalog.company_name)
        var semen_catalog_id_input = modal.find('input[name=semen_catalog_id]')
        if (semen_catalog_id_input.length == 1) {
            semen_catalog_id_input.val(semen_catalog.id)
        }
        else {
            semen_catalog_id_input = "<input id='semen_catalog_id' type='hidden' class='form-control' name='semen_catalog_id'>";
            modal.find('#bull_name').after(semen_catalog_id_input)
            semen_catalog_id_input = modal.find('input[name=semen_catalog_id]')
            semen_catalog_id_input.val(semen_catalog.id)
        }
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Semen Catalog Record")
        modal.find('input[name=semen_catalog_id]').remove()
    }
})
$('#editAiRecordInputModal').on('show.bs.modal', function (event) {
    var event_source = $(event.relatedTarget);
    var modal = $(this);
    var ai_record_id = event_source.parent().parent().attr('data-src');
    if (event_source.attr('id') == 'aiRecordEditBtn' | event_source.attr('id') == 'aiRecordEditBtn2') {
        modal.find('.modal-title').text("Edit Insemination Record")
        var ai_record = JSON.parse(myStorage.getItem('ai_record_' + ai_record_id))
        modal.find('#service_date').val(ai_record.service_date)
        modal.find('#bull_code').val(ai_record.bull_code)
        modal.find('#bull_name').val(ai_record.bull_name)
        modal.find('#inbreeding_status').val(ai_record.inbreeding_status)
        modal.find('#ai_cost').val(ai_record.ai_cost)
        modal.find('#open_days').val(ai_record.open_days)
        modal.find('#repeats').val(ai_record.repeats)
        modal.find('#vet_name').val(ai_record.vet_name)
        ai_record_id_input = modal.find('input[name=ai_record_id]')
        ai_record_id_input.val(ai_record.id)
    }
    else {
        clearTextAndNumberInputFields(modal);
    }
})
$('#pregnancyDiagnosisInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var pregnancy_diagnosis_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'pregnancyDiagnosisEditBtn') {
        modal.find('.modal-title').text("Edit Pregnancy Diagnosis Record")
        var ai_record = JSON.parse(myStorage.getItem('pregnancy_diagnosis_id' + pregnancy_diagnosis_id))
        modal.find('#pregnancy_diagnosis_date').val(ai_record.pregnancy_diagnosis_date)
        modal.find('#pregnancy_diagnosis_result').val(ai_record.pregnancy_diagnosis_result)
        modal.find('#pregnancy_diagnosis_cost').val(ai_record.pregnancy_diagnosis_cost)
        modal.find('#pregnancy_diagnosis_vet_name').val(ai_record.pregnancy_diagnosis_vet_name)
        modal.find('select[name=ai_record_id]').val(ai_record.id)
    } else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Pregnancy Diagnosis Record")
        modal.find('select[name=ai_record_id]').val('ai_record_id')
    }
})
$('#pregnancyCalendarEditModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var pregnancy_calendar_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'pregnancyCalendarEditBtn') {
        modal.find('.modal-title').text("Edit Pregnancy Calendar")
        var ai_record = JSON.parse(myStorage.getItem('pregnancy_calendar_id' + pregnancy_calendar_id))
        modal.find('input[name=ai_record_id]').val(ai_record.id)
        modal.find('#first_heat_check_date').val(ai_record.first_heat_check_date)
        modal.find('#second_heat_check_date').val(ai_record.second_heat_check_date)
        modal.find('#pregnancy_diagnosis_date').val(ai_record.pregnancy_diagnosis_date)
        modal.find('#drying_date').val(ai_record.drying_date)
        modal.find('#steaming_date').val(ai_record.steaming_date)
        modal.find('#due_date').val(ai_record.due_date)
    }
})
$('#insuranceInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var insurance_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'insuranceEditBtn') {
        modal.find('.modal-title').text("Edit Insurance Details")
        var insurance = JSON.parse(myStorage.getItem('insurance_' + insurance_id))
        var insurance_id_input = modal.find('input[name=insurance_id]')
        if (insurance_id_input.length == 1) {
            insurance_id_input.val(insurance.id)
        }
        else {
            insurance_id_input = "<input id='insurance_id' type='hidden' class='form-control' name='insurance_id'>";
            modal.find('#from_date').after(insurance_id_input)
            insurance_id_input = modal.find('input[name=insurance_id]')
            insurance_id_input.val(insurance.id)
        }
        modal.find('#cow_id').val(insurance.cow_id)
        modal.find('#from_date').val(insurance.from_date)
        modal.find('#to_date').val(insurance.to_date)
        modal.find('#insured_value').val(insurance.insured_value)
        modal.find('#premium_amount').val(insurance.premium_amount)
        modal.find('#insurance_policy').val(insurance.policy)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('input[name=insurance_id]').remove()
        modal.find('#cow_id').val("cow_id")
        modal.find('#from_date').val(current_date_string)
        modal.find('#to_date').val(current_date_string)
    }
})
$('#incomeInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var income_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'incomeEditBtn') {
        modal.find('.modal-title').text("Edit Income Details")
        var income = JSON.parse(myStorage.getItem('income_' + income_id))
        var income_id_input = modal.find('input[name=income_id]')
        if (income_id_input.length == 1) {
            income_id_input.val(income.id)
        }
        else {
            income_id_input = "<input id='income_id' type='hidden' class='form-control' name='income_id'>";
            modal.find('#income_date').after(income_id_input)
            income_id_input = modal.find('input[name=income_id]')
            income_id_input.val(income.id)
        }
        modal.find('#income_date').val(income.date)
        modal.find('#income_amount').val(income.amount)
        modal.find('#income_source').val(income.source)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Income Record")
        modal.find('input[name=income_id]').remove()
        modal.find('#income_date').val(current_date_string)
    }
})
$('#expenseInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var expense_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'expenseEditBtn') {
        modal.find('.modal-title').text("Edit Expense Details")
        var expense = JSON.parse(myStorage.getItem('expense_' + expense_id))
        var expense_id_input = modal.find('input[name=expense_id]')
        if (expense_id_input.length == 1) {
            expense_id_input.val(expense.id)
        }
        else {
            expense_id_input = "<input id='expense_id' type='hidden' class='form-control' name='expense_id'>";
            modal.find('#expense_date').after(expense_id_input)
            expense_id_input = modal.find('input[name=expense_id]')
            expense_id_input.val(expense.id)
        }
        modal.find('#expense_date').val(expense.date)
        modal.find('#expense_amount').val(expense.amount)
        modal.find('#expense_source').val(expense.source)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Expense Record")
        modal.find('input[name=expense_id]').remove()
        modal.find('#expense_date').val(current_date_string)
    }
})
$('#cowDiseaseInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var disease_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'diseaseEditBtn') {
        modal.find('.modal-title').text("Edit Disease Details")
        var disease = JSON.parse(myStorage.getItem('disease_' + disease_id))
        var disease_id_input = modal.find('input[name=disease_id]')
        if (disease_id_input.length == 1) {
            disease_id_input.val(disease.id)
        }
        else {
            disease_id_input = "<input id='disease_id' type='hidden' class='form-control' name='disease_id'>";
            modal.find('#date_discovered').after(disease_id_input)
            disease_id_input = modal.find('input[name=disease_id]')
            disease_id_input.val(disease.id)
        }
        modal.find('#date_discovered').val(disease.date_discovered)
        modal.find('#disease_name').val(disease.name)
        modal.find('#disease_details').val(disease.details)
    }
    else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Disease Record")
        modal.find('input[name=disease_id]').remove()
        modal.find('#date_discovered').val(current_date_string)
    }
})
$('#abortionsInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var abortion_miscarriage_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'abortionEditBtn') {
        modal.find('.modal-title').text("Edit Abortion Record")
        var abortion_miscarriage_record = JSON.parse(myStorage.getItem
            ('abortion_miscarriage_id_' + abortion_miscarriage_id))
        modal.find('#event_date').val(abortion_miscarriage_record.event_date)
        modal.find('#event_type').val(abortion_miscarriage_record.event_type)
        modal.find('#event_cause').val(abortion_miscarriage_record.event_cause)
        modal.find('#event_cost').val(abortion_miscarriage_record.event_cost)
        modal.find('#vet_name').val(abortion_miscarriage_record.vet_name)
        modal.find('select[name=ai_record_id]').val(abortion_miscarriage_record.id)
    } else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Abortion Record")
        modal.find('select[name=ai_record_id]').val('ai_record_id')
    }
})
$('#calvingInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var calving_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'calvingEditBtn') {
        modal.find('.modal-title').text("Edit Calving Record")
        var calving_record = JSON.parse(myStorage.getItem('calving_' + calving_id))
        modal.find('#calf_code').val(calving_record.calf_code)
        modal.find('#calf_name').val(calving_record.calf_name)
        modal.find('#calving_date').val(calving_record.calving_date)
        modal.find('#calf_sex').val(calving_record.calf_sex)
        modal.find('#calving_type').val(calving_record.calving_type)
        modal.find('#calf_breed').val(calving_record.calf_breed)
        modal.find('#calf_color').val(calving_record.calf_color)
        modal.find('#calf_weight').val(calving_record.calf_weight)
        modal.find('select[name=ai_record_id]').val(calving_record.id)
    } else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Calving Record")
        modal.find('select[name=ai_record_id]').val('ai_record_id')
    }
})
$('#feedItemInputDialog').on('show.bs.modal', function (event) {
    var modal = $(this)
    var feed_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'feedItemEditBtn') {
        modal.find('.modal-title').text("Edit Feed Item")
        var feed_item = JSON.parse(myStorage.getItem('feed_item_' + feed_id))
        modal.find('#item_name').val(feed_item.name)
        modal.find('#item_unit_measure').val(feed_item.unit_of_measure)
        modal.find('#item_unit_price').val(feed_item.unit_price)
        modal.find('#item_available_stock').val(feed_item.initial_stock)
        modal.find('#item_reorder_level').val(feed_item.reorder_level)
    } else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Feed Item Record")
    }
})
$('#feedingProgramInputDialog').on('show.bs.modal', function (event) {
    var modal = $(this)
    var feeding_programme_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'feedingProgrammeEditBtn') {
        modal.find('.modal-title').text("Edit Feeding Programme")
        var feeding_programme = JSON.parse(myStorage.getItem('feeding_programme_' + feeding_programme_id))
        var feeding_programme_id_input = modal.find('input[name=feeding_programme_id]')
        if (feeding_programme_id_input.length == 1) {
            feeding_programme_id_input.val(feeding_programme.id)
        }
        else {
            feeding_programme_id_input = "<input id='feeding_programme_id' type='hidden' class='form-control' name='feeding_programme_id'>";
            modal.find('#feed_quantity').after(feeding_programme_id_input)
            feeding_programme_id_input = modal.find('input[name=feeding_programme_id]')
            feeding_programme_id_input.val(feeding_programme.id)
        }
        modal.find('#feed_quantity').val(feeding_programme.quantity)
        modal.find('select[name=feeding_category]').val(feeding_programme.feeding_category)
        modal.find('select[name=feed_formulation_id]').val(feeding_programme.feed_formulation_id)
    } else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Feeding Programme Record")
        modal.find('input[name=feeding_programme_id').remove();
        modal.find('select[name=feed_formulation_id]').val('Select Feed Formulation')
        modal.find('select[name=feeding_category]').val('Select Group')
    }
})
$('#feedFormulationInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var feeding_formulation_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'feedFormulationEditBtn') {
        modal.find('.modal-title').text("Edit Feed Formulation")
        var feeding_formulation = JSON.parse(myStorage.getItem('feeding_formulation_' + feeding_formulation_id))
        var feeding_formulation_id_input = modal.find('input[name=feeding_formulation_id]')
        if (feeding_formulation_id_input.length == 1) {
            feeding_programme_id_input.val(feeding_formulation.id)
        }
        else {
            feeding_formulation_id_input = "<input id='feeding_formulation_id' type='hidden' class='form-control' name='feeding_formulation_id'>";
            modal.find('#feed_quantity').after(feeding_formulation_id_input)
            feeding_formulation_id_input = modal.find('input[name=feeding_formulation_id]')
            feeding_formulation_id_input.val(feeding_formulation.id)
        }
        modal.find('#feed_formulation_quantity').val(feeding_formulation.quantity)
        modal.find('#feed_formulation_name').val(feeding_formulation.name)
        modal.find('select[name=feed_item]').val('Select Item')
        modal.find('input[name=feed_formulation_part_quantity]').val(0)
    } else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Feed Formulation Record")
        modal.find('input[name=feeding_formulation_id').remove();
        modal.find('select[name=feed_item]').val('Select Item')
    }
})
$('#feedFormulationItemInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var feeding_formulation_part_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'feedFormulationPartEditBtn') {
        modal.find('.modal-title').text("Edit Feed Formulation Item")
        var feed_item_part = JSON.parse(myStorage.getItem('feeding_formulation_part_' + feeding_formulation_part_id))
        var feeding_formulation_part_id_input = modal.find('input[name=feed_form_part_id]')
        console.log(feed_item_part)
        feeding_formulation_part_id_input.val(feed_item_part.id)
        modal.find('#feed_form_part_quantity').val(feed_item_part.quantity)
    } else {
        clearTextAndNumberInputFields(modal);
    }
})
$('#cowBodyTraitsInputModal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var body_traits_id = $(event.relatedTarget).parent().parent().attr('data-src');
    if ($(event.relatedTarget).attr('id') == 'cowBodyTraitsEditBtn') {
        modal.find('.modal-title').text("Edit Body Traits Record")
        var body_traits = JSON.parse(myStorage.getItem('body_traits_' + body_traits_id))
        modal.find('#cow_id').val(body_traits.id)
        modal.find('#frame').val(body_traits.frame)
        modal.find('#dairy_strength').val(body_traits.dairy_strength)
        modal.find('#udder').val(body_traits.udder)
        modal.find('#feet_legs').val(body_traits.feet_legs)
        modal.find('#stature').val(body_traits.stature)
        modal.find('#chest_width').val(body_traits.chest_width)
        modal.find('#body_depth').val(body_traits.body_depth)
        modal.find('#angularity').val(body_traits.angularity)
        modal.find('#cond_score').val(body_traits.cond_score)
        modal.find('#thurl_width').val(body_traits.thurl_width)
        modal.find('#rump_angle').val(body_traits.rump_angle)
        modal.find('#rump_width').val(body_traits.rump_width)
        modal.find('#right_legs_rv').val(body_traits.right_legs_rv)
        modal.find('#right_legs_sv').val(body_traits.right_legs_sv)
        modal.find('#foot_angle').val(body_traits.foot_angle)
        modal.find('#locomotion').val(body_traits.locomotion)
    } else {
        clearTextAndNumberInputFields(modal);
        modal.find('.modal-title').text("Add Body Traits Record")
        modal.find('select[name=cow_id]').val('cow_id')
    }
})

setPagination = function (tablesToAddPaginationTo) {
    tablesToAddPaginationTo.forEach(function (table) {
        $(table).DataTable({
            "processing": true,
            "columnDefs": [
                {
                    "targets": ':contains(Actions)',
                    "visible": true,
                    "searchable": false
                },
            ],
            dom: 'Bfrtip',
            buttons: [
	            {
	                extend: 'print',
	                exportOptions: {
		                columns: ':not(:contains(Actions))'
		            }
	            },
	            {
	                extend: 'excel',
	                exportOptions: {
		                columns: ':not(:contains(Actions))'
		            }
	            },
	        ],
        });
    });
}
$(document).ready(function () {
    // select values passed to the client from the server
    var selectedMonth = window.month;
    var selectedYear = window.year;
    var selectedClient = window.client;
    var selectedConsumer = window.consumer;
    var selectedCow = window.selectedCow;
    $('select[name=month]').val(selectedMonth);
    $('input[name=year]').val(selectedYear);
    $('select[name=client_id]').val(selectedClient);
    $('select[name=consumer_id]').val(selectedConsumer);
    $('select[id=selectedMilkProdHistoryCow]').val(selectedCow);
    //	configure milk production table pagination
    var tablesToAddPaginationTo = ['#milkProductionTable', '#milkProductionTargetsTable', '#monthlyMilkProductionTable', '#clientsTable', '#consumersTable', '#dailyMilkConsumptionTable', '#dailyMilkSalesTable', '#salesSummaryTable', '#consumptionSummaryTable', '#cowsTable', '#cowWeightsTable', '#calvesGrowthTable', '#calfFeedingTable', '#cowSalesTable', '#cowTreatmentsTable', '#cowDewormingTable', '#cowVaccinationsTable', '#cowDeathsTable', '#cowAutopsiesTable', '#cowSemenCatalogTable', '#cowAiRecordsTable', '#failedIseminationsTable', '#inseminationsHistoryTable', '#pregnancyDiagnosisTable', '#pregnancyCalendarTable', '#calvingsTable', '#abortionsTable', '#cowInsuranceTable', '#incomeTable', '#expensesTable', '#employeesTable', '#salaryAdvancesTable', '#salariesTable', '#feedItemsTable', '#feedingProgrammesTable', '#feedingFormulationsTable', '#cowDiseasesTable', '#breedingStatisticsTable']
    setPagination(tablesToAddPaginationTo);
});

$('#milkInputForm').on('submit', function (event) {
    event.preventDefault();
    var submitForm = $(this);
    var formData = $('#milkInputForm').serialize();
    $.post(postUrl + '/digitaldairy/save_milk_production', formData, function (data) {
        myStorage.setItem('milk_p_' + data.id, JSON.stringify(data))
        var tableRow = $('tr[data-src=' + data.id + ']')
        if (tableRow.length == 0) {
            tableRow = $($('#milkProductionTable tbody tr')[0])
        }
        else {
            $('#milkProductionTable').DataTable().row(tableRow).remove();
        }
        tableRow = tableRow.clone();
        tableRow.attr('data-src', data.id);
        tableRow.attr('hidden', false);
        tableRow.children('script').remove();
        tableRow.children('td')[0].innerText = data.cow_id;
        tableRow.children('td')[1].innerHTML = '<a href=' + data.milk_production_url + '>' + data.cow_name + '</a>';
        tableRow.children('td')[2].innerText = data.am_quantity;
        tableRow.children('td')[3].innerText = data.noon_quantity;
        tableRow.children('td')[4].innerText = data.pm_quantity;
        tableRow.children('td')[5].innerText = (parseFloat(data.am_quantity) + parseFloat(data.noon_quantity) + parseFloat(data.pm_quantity)).toFixed(2);
        tableRow.find('form > input[name=milk_production_id]').val(data.id)
        tableRow.find('form').attr('id', 'deleteMilkProductionForm' + data.id)
        tableRow.find('button[type=submit]').attr('form', 'deleteMilkProductionForm' + data.id)
        $('#milkProductionTable').DataTable().row.add(tableRow).draw();
        //clear or remove value from the input
        $('#cow_id').val('cow_id')
        clearTextAndNumberInputFields(submitForm);
        if ($.find('.modal-title:contains("Edit")').length == 1) {
            //close the modal
            $(submitForm.parents('div.modal')).modal('toggle');
        }
    })
    return false;
});
$('form[id^=deleteMilkProductionForm]').on('submit', function (event) {
    event.preventDefault();
    var deleteForm = $(this);
    var formData = deleteForm.serialize();
    $.post(postUrl + '/digitaldairy/delete_milk_production', formData, function (data) {
        deleteForm.parents('table').DataTable().row(deleteForm.parents('tr')).remove().draw();
    })
    return false;
});
$('form[id^=deleteMilkProductionTargetForm]').on('submit', function (event) {
    event.preventDefault();
    var deleteForm = $(this);
    var formData = deleteForm.serialize();
    $.post(postUrl + '/digitaldairy/delete_milk_production_target', formData, function (data) {
        deleteForm.parents('table').DataTable().row(deleteForm.parents('tr')).remove().draw();
    })
    return false;
});
$('form[id=feedFormulationPartInputForm]').on('submit', function (event) {
    event.preventDefault();
    var form = $(this);
    var formData = form.serialize();
    $.post(postUrl + '/digitaldairy/save_feed_formulation_part', formData, function (data) {
        myStorage.setItem('feeding_formulation_part_' + data.id, JSON.stringify(data));
        //clear a field
        form.find('input[name=feed_form_part_quantity]').val('')
    })
    return false;
});
$('form[id=feedFormulationInputForm]').on('submit', function (event) {
    event.preventDefault();
    var form = $(this);
    var formData = form.serialize();
    $.post(postUrl + '/digitaldairy/save_feed_formulation', formData, function (data) {
//        myStorage.setItem('feeding_formulation_' + data.id, JSON.stringify(data));
        //clear the required fields
        var myDocument = $(data)
        $('div.table-responsive').parent('div')[0].innerHTML = myDocument.find('div.table-responsive')[0].outerHTML;
        var scriptWithData = myDocument.find('div.container-fluid script')
        $('div.container-fluid').after(scriptWithData);
        form.find('select[name=feed_item]').val('Select Item')
        form.find('input[name=feed_formulation_part_quantity]').val('')
    })
    return false;
});
$('#targetInputForm').on('submit', function (event) {
    event.preventDefault();
    var modal = $(this).parents('div.modal');
    var formData = $('#targetInputForm').serialize();
    $.post(postUrl + '/digitaldairy/save_daily_milk_target', formData, function (data) {
        myStorage.removeItem('milk_p_target_' + data.cow_id);
        myStorage.setItem('milk_p_target_' + data.cow_id, JSON.stringify(data))
        var tableRow = $('tr[data-src=' + data.cow_id + ']')
        if (tableRow.length == 0) {
            tableRow = $($('#milkProductionTargetsTable tbody tr')[0])
        }
        else {
            $('#milkProductionTargetsTable').DataTable().row(tableRow).remove();
        }
        tableRow = tableRow.clone();
        tableRow.attr('data-src', data.cow_id);
        tableRow.attr('hidden', false);
        tableRow.children('script').remove();
        tableRow.children('td')[0].innerText = data.cow_id;
        tableRow.children('td')[1].innerText = data.cow_name;
        tableRow.children('td')[2].innerHTML = data.target_quantity;
        tableRow.find('form > input[name=cow_id]').val(data.cow_id)
        tableRow.find('form').attr('id', 'deleteMilkProductionTargetForm' + data.cow_id)
        tableRow.find('button[type=submit]').attr('form', 'deleteMilkProductionTargetForm' + data.cow_id);
        modal.find('#cow_id').val('cow_id');
        $('#milkProductionTargetsTable').DataTable().row.add(tableRow).draw();
        clearTextAndNumberInputFields(modal);
    })
    return false;
});
$(function () {
    var canvases;
    function init() {
        canvases = document.getElementsByTagName('canvas');
        for (var i = 0; i < canvases.length; i++) {
            var canvas = canvases[i];
            if (canvas.getContext) {
                var ctx = canvas.getContext('2d');
                window.addEventListener('resize', resizeCanvas, false);
                window.addEventListener('orientationchange', resizeCanvas, false)
                resizeCanvas();
            }
        }
    }
    function resizeCanvas() {
        for (var i = 0; i < canvases.length; i++) {
            var canvas = canvases[i];
            // set up temporary canvas
            var tempCanvas = document.createElement('canvas');
            tempCanvas.width = canvas.width;
            tempCanvas.height = canvas.height;
            var tempCtx = tempCanvas.getContext('2d');
            // copy to temporary canvas
            tempCtx.drawImage(canvas, 0, 0);
            // resize the original canvas
            if (window.innerWidth <= 400) {
                canvas.width = window.innerWidth;
                canvas.height = (window.innerWidth * 2);
            }
            // copy canvas as image data 
            var ctx = canvas.getContext('2d');
            // copy back to resized canvas 
            ctx.drawImage(tempCanvas, 0, 0, tempCanvas.width, tempCanvas.height, 0, 0, canvas.width, canvas.height);
        }
    }
    init();
    // configure the yearly milk_production chart
    var yearlyMilkProductionChart = document.getElementById('yearlyMilkProductionChart');
    if (yearlyMilkProductionChart == undefined) {
        return;
    }
    var yearlyMilkProductionChartCtx = yearlyMilkProductionChart.getContext('2d');
    monthlyMilkProductionList = JSON.parse(myStorage.getItem('monthlyMilkProductionList'))
    month_data = []
    monthlyMilkProductionList.forEach(function (item, index) {
        month_data[item.month - 1] = item.quantity;
    })
    var chart = new Chart(yearlyMilkProductionChartCtx, {
        // The type of chart we want to create
        type: 'line',
        // The data for our dataset
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            datasets: [{
                label: 'Monthly Milk Production',
                backgroundColor: 'rgb(175, 183, 191)',
                borderColor: 'rgb(31, 37, 43)',
                data: month_data
            }]
        },

        // Configuration options go here
        options: {
            title: {
                text: "Yearly Milk Production Chart",
                display: true,
            }
        }
    });
});
$(function () {
    // configure the monthly milk production chart
    var monthlyMilkProductionChart = document.getElementById('monthlyMilkProductionChart');
    if (monthlyMilkProductionChart == undefined) {
        return;
    }
    var monthlyMilkProductionChartCtx = monthlyMilkProductionChart.getContext('2d');
    dailyMilkProductionList = JSON.parse(myStorage.getItem('dailyMilkProductionList'))
    day_labels = []
    day_data = []
    dailyMilkProductionList.forEach(function (item, index, array) {
        day_labels.push(item.day);
        day_data.push(item.quantity);
    })
    var chart = new Chart(monthlyMilkProductionChartCtx, {
        // The type of chart we want to create
        type: 'line',
        // The data for our dataset
        data: {
            labels: day_labels,
            datasets: [{
                label: 'Daily Milk Production',
                backgroundColor: 'rgb(175, 183, 191)',
                borderColor: 'rgb(31, 37, 43)',
                data: day_data
            }]
        },

        // Configuration options go here
        options: {
            title: {
                text: "Monthly Milk Production Chart",
                display: true,
            }
        }
    });
});
$(function () {
    // configure the yearly milk sales chart
    var yearlyMilkSalesChart = document.getElementById('yearlyMilkSalesChart')
    if (yearlyMilkSalesChart == undefined) {
        return;
    }
    var yearlyMilkSalesChartCtx = yearlyMilkSalesChart.getContext('2d');
    monthlyMilkSalesList = JSON.parse(myStorage.getItem('monthlyMilkSalesList'))
    month_milk_sales_data = []
    monthlyMilkSalesList.forEach(function (item, index) {
        month_milk_sales_data[item.month - 1] = item.quantity;
    })
    var chart = new Chart(yearlyMilkSalesChartCtx, {
        // The type of chart we want to create
        type: 'line',
        // The data for our dataset
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            datasets: [{
                label: 'Monthly Milk Sales',
                backgroundColor: 'rgb(175, 183, 191)',
                borderColor: 'rgb(31, 37, 43)',
                data: month_milk_sales_data
            }]
        },

        // Configuration options go here
        options: {
            title: {
                text: "Yearly Milk Sales Chart",
                display: true,
            }
        }
    });
});
$(function () {
    // configure the monthly milk sales chart
    var monthlyMilkSalesChart = document.getElementById('monthlyMilkSalesChart')
    if (monthlyMilkSalesChart == undefined) {
        return;
    }
    var monthlyMilkSalesChartCtx = monthlyMilkSalesChart.getContext('2d');
    dailyMilkSaleList = JSON.parse(myStorage.getItem('dailyMilkSaleList'))
    day_labels = []
    day_milk_sales_data = []
    dailyMilkSaleList.forEach(function (item, index) {
        day_labels.push(item.day);
        day_milk_sales_data.push(item.quantity);
    })
    var chart = new Chart(monthlyMilkSalesChartCtx, {
        // The type of chart we want to create
        type: 'line',
        // The data for our dataset
        data: {
            labels: day_labels,
            datasets: [{
                label: 'Daily Milk Sales',
                backgroundColor: 'rgb(175, 183, 191)',
                borderColor: 'rgb(31, 37, 43)',
                data: day_milk_sales_data
            }]
        },

        // Configuration options go here
        options: {
            title: {
                text: "Monthly Milk Sales Chart",
                display: true,
            }
        }
    });
});
