window.addEventListener('load', () => {
  odoo.define('customizeme', require => {
    const publicWidget = require('web.public.widget')
    let websiteSale = null

    const productForm = Array.from(document.querySelectorAll('form')).find(el =>
      el.action.includes('/shop/cart/update')
    )
    const productId = productForm.elements.product_template_id.value

    fetch('/customizeme/data?product_id=' + productId)
      .then(r => r.json())
      .then(data => {
        const { accessKey, attributes, customInjectTo, injectTo, productUrl } = data
        if (!productUrl || !accessKey) return

        let root
        if (customInjectTo || injectTo) {
          try {
            root = document.querySelector(customInjectTo || injectTo)
          } catch (err) {
            console.log(err)
          }
        }
        if (!root) root = document.getElementById('customizeme_root')

        const iframe = document.createElement('iframe')
        iframe.style.display = 'none'
        iframe.src = productUrl
        iframe.onload = () => {
          iframe.contentWindow.postMessage({ type: 'init', accessKey }, '*')
          Object.assign(iframe.style, {
            display: 'block',
            outline: 'none',
            border: 'none',
            width: '100%',
            height: '100%',
            position: 'absolute',
            left: 0,
            top: 0
          })
          if (root.style.display === 'none') root.style.display = 'block'
          root.style.position = 'relative'
        }
        root.appendChild(iframe)

        const callEvent = eventData => {
          iframe.contentWindow.postMessage({ type: 'call_event', eventData }, '*')
        }

        const setMaterialToPart = (partName, materialName) => {
          const eventData = { type: 'SET_MATERIAL_TO_PART_BY_NAMES', args: [partName, materialName] }
          callEvent(eventData)
        }

        const setOptionalPartToPart = (partName, optionalPartName) => {
          const eventData = { type: 'SET_OPTIONAL_PART_TO_PART_BY_NAMES', args: [partName, optionalPartName] }
          callEvent(eventData)
        }

        const setSuggestion = (partName, suggestionName) => {
          const eventData = { type: 'SET_CUSTOMIZATION_SUGGESTION', args: [suggestionName] }
          callEvent(eventData)
        }

        const callbacks = {
          material: setMaterialToPart,
          optionalPart: setOptionalPartToPart,
          suggestion: setSuggestion
        }

        if (productForm) {
          const attributesSelects = Array.from(productForm.elements).filter(el => el.type === 'select-one')

          attributesSelects.forEach(select => {
            const attribute = attributes.find(el => String(el.id) === select.getAttribute('data-attribute_id'))
            if (attribute) {
              const callback = callbacks[attribute.type]
              if (callback) {
                const callCallback = () =>
                  callback(attribute.partName, select.selectedOptions[0].getAttribute('data-value_name'))
                window.addEventListener('message', ({ data }) => {
                  if (data.type === 'customizeme_configuration_loaded') {
                    select.addEventListener('change', callCallback)
                    callCallback()
                  }
                })

                callCallback()
              }
            }
          })

          const refreshForm = () => {
            if (!publicWidget.registry.WebsiteSale) return
            if (!websiteSale) {
              websiteSale = new publicWidget.registry.WebsiteSale()
            }
            const select = attributesSelects[0]
            select && websiteSale.onChangeVariant({ currentTarget: select, target: select })
          }

          window.addEventListener('message', ({ data }) => {
            if (data.type === 'customizeme_data') {
              data.data.forEach(customizationPart => {
                const attribute = attributes.find(
                  el => customizationPart.displayName === el.partName || customizationPart.name === el.partName
                )
                if (!attribute || attribute.type === 'suggestion') return
                const select = attributesSelects.find(
                  el => el.getAttribute('data-attribute_id') === String(attribute.id)
                )
                if (!select) return

                const resourceName =
                  attribute.type === 'material' ? customizationPart.materialName : customizationPart.optionalPartName
                Array.from(select.options).forEach(option => {
                  if (resourceName === option.getAttribute('data-value_name')) {
                    select.value = option.value
                  }
                })
              })
              refreshForm()
            }
          })
        }
      })
      .catch(console.log)
  })
})
