import MaskedInput, { conformToMask } from 'vue-text-mask'
import inputValidations from '../lib/input_validations'
import { formatDollars } from '../lib/dollars'
import { emitFieldChange } from '../lib/emitters'

export default {
  name: 'textinput',

  components: {
    MaskedInput,
  },

  props: {
    name: String,
    validation: {
      type: String,
      default: () => 'anything',
    },
    initialValue: {
      type: String,
      default: () => '',
    },
    initialErrors: {
      type: Array,
      default: () => [],
    },
    paragraph: String,
    noMaxWidth: String,
    optional: Boolean,
  },

  data: function() {
    return {
      showError: (this.initialErrors && this.initialErrors.length) || false,
      showValid: false,
      mask: inputValidations[this.validation].mask,
      pipe: inputValidations[this.validation].pipe || undefined,
      keepCharPositions:
        inputValidations[this.validation].keepCharPositions || false,
      validationError:
        this.initialErrors.join(' ') ||
        inputValidations[this.validation].validationError,
      value: this.initialValue,
      modified: false,
    }
  },

  computed: {
    rawValue: function() {
      return this._rawValue(this.value)
    },
  },

  mounted: function() {
    if (this.value) {
      this._checkIfValid({ value: this.value, invalidate: true })

      if (this.mask && this.validation !== 'email') {
        const mask =
          typeof this.mask.mask !== 'function'
            ? this.mask
            : mask.mask(this.value).filter(val => val !== '[]')

        this.value = conformToMask(this.value, mask).conformedValue
      }
    }
  },

  created: function() {
    this.$root.$emit('field-mount', {
      name: this.name,
      optional: this.optional,
    })
  },

  methods: {
    // When user types a character
    onInput: function(e) {
      // When we use the native textarea element, we receive an event object
      // When we use the masked-input component, we receive the value directly
      const value = typeof e === 'object' ? e.target.value : e
      this.value = value
      this.modified = true
      this._checkIfValid({ value })
    },

    // When field is blurred (un-focused)
    onChange: function(e) {
      // Only invalidate the field when it blurs
      this._checkIfValid({ value: e.target.value, invalidate: true })
    },

    onBlur: function(e) {
      if (!(this.optional && e.target.value === '')) {
        this._checkIfValid({ value: e.target.value.trim(), invalidate: true })
      }
      this.value = e.target.value.trim()

      if (this.validation === 'dollars') {
        this.value = formatDollars(this._rawValue(e.target.value))
      }
    },

    //
    _checkIfValid: function({ value, invalidate = false }) {
      // Validate the value
      let valid = this._validate(value)

      if (!this.modified && this.initialErrors && this.initialErrors.length) {
        valid = false
      } else if (this.optional && value === '') {
        valid = true
      }

      if (this.modified) {
        this.validationError = inputValidations[this.validation].validationError
      }

      // Show error messages or not
      if (valid) {
        this.showError = false
      } else if (invalidate) {
        this.showError = true
      }
      this.showValid = this.value != '' && valid

      // Emit a change event
      emitFieldChange(this, {
        value: this._rawValue(value),
        valid,
        name: this.name,
      })
    },

    _rawValue: function(value) {
      return inputValidations[this.validation].unmask.reduce(
        (currentValue, character) => {
          return currentValue.split(character).join('')
        },
        value
      )
    },

    _validate: function(value) {
      return inputValidations[this.validation].match.test(this._rawValue(value))
    },
  },
}
