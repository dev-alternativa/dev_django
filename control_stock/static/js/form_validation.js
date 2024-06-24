/**  VALIDAÇÕES DO FORMULÁRIO DE CLIENTE/FORNECEDOR  **/
document.addEventListener('DOMContentLoaded', function () {
  // Captura o formulário
  const form = document.getElementById('form_cliente_fornecedor');
  if(form){

    // Captura todas as abas
    const tabs = document.querySelectorAll('.nav-link');
    // captura os paineis das abas
    const tabPanes = document.querySelectorAll('.tab-pane');
  
    // Remove `required` dos campos em abas inativas ao carregar a página
    tabPanes.forEach(tabPane => {
      if(!tabPane.classList.contains('active')){
        const inputs = tabPane.querySelectorAll('[required]');
        inputs.forEach(input => {
          input.dataset.required = 'true';
          input.removeAttribute('required');
        });
      }
    });
  
    // Adiciona/remove `required` mudar de aba
    tabs.forEach(tab => {
      tab.addEventListener('show.bs.tab', function(event){
        const targetTabPane = document.querySelector(event.target.getAttribute('href'));
        const previousTabPane = document.querySelector(event.relatedTarget.getAttribute('href'));
  
        // Adiciona `required` ao mudar de aba
        const activeInputs = targetTabPane.querySelectorAll("[data-required='true']");
        activeInputs.forEach(input => {
          input.setAttribute('required', 'true');
        })
  
        // Remove `required dos campos da aba inativa
        const inactiveInputs = previousTabPane.querySelectorAll('[required]');
        inactiveInputs.forEach(input => {
          input.removeAttribute('required');
        });
      });
    });
  
    // Valida o formulário na submissão
    form.addEventListener('submit', function(event){
      if(!form.checkValidity()){
        event.preventDefault();
        event.stopPropagation();
  
        // Encontra o primeiro campo inválido
        const firstinvalidField = form.querySelector(':invalid');
  
        if(firstinvalidField){
          // Econtra a aba que contém o campo inválido
          const invalidFieldTabPane = firstinvalidField.closest('.tab-pane');
          if(invalidFieldTabPane){
            const tabId = invalidFieldTabPane.id;
            // Ativa a aba correspondente
            const tabToActivate = document.querySelector(`a[href="#${tabId}"]`);
            if(tabToActivate){
              $(tabToActivate).tab('show');
            }
          }
  
          // Define o foco no primeiro campo inválido após a aba ser ativada
          firstinvalidField.focus();
        }
      }
      form.classList.add('was-validated');
    }, false);
  }
});
