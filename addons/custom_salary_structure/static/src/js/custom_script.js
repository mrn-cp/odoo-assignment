
function handleChange(event) {
    var changedField = event.target.dataset.field;
    var changedValue = event.target.value;
    var changedId = event.target.dataset.paramId
    var changedType = event.target.dataset.paramType

    if (parseFloat(changedValue) < 0) {
            document.querySelector('[data-param-id="' + changedId + '"]').value = 0 ;
            return
        }
    else {

           // Deduction amount calculation
           deductionNode = document.querySelectorAll('[data-param-type="deduction"]')
           var totalDed = 0.0;
           for (let i = 0; i < deductionNode.length; i++ ) {
              if (deductionNode[i].value == null) {
                deductionNode[i].value = 0.0
              }
              totalDed += parseFloat(deductionNode[i].value);
            }

           // Other amount calculation
           otherNode = document.querySelectorAll('[data-param-type="other"]')
           var otherAmt = 0.0;
           for (let i = 0; i < otherNode.length; i++ ) {
              if (otherNode[i].value == null) {
                otherNode[i].value = 0.0
              }
              otherAmt += parseFloat(otherNode[i].value);
            }

           // Base Amount
           var baseValue = parseFloat(document.querySelector('.input-field1').value);
           newBaseValue = baseValue - totalDed -otherAmt;

           // if base amount is zero raise warning
           if (newBaseValue <= 0) {
                window.alert("Base Amount should not less than or equal to zero.");
           }

           document.querySelector('.input-field').value = newBaseValue;

    }
}

function myJavaScriptFunction() {
      var updatedData = {}

      var inputElements = document.querySelectorAll('[data-param-type="deduction"], [data-param-type="other"]');

      inputElements.forEach(function(element) {
          var paramId = element.getAttribute('data-param-id');
          var paramType = element.getAttribute('data-param-type');
          var amount = parseFloat(element.value);
          updatedData[paramId] = amount;
      });

      var baseElement = document.querySelector('.input-field');
      var base_id = baseElement.getAttribute('data-param-id');
      var base_amount = parseFloat(baseElement.value);
      updatedData[base_id] = base_amount;

      return updatedData
}
