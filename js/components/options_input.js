export default {
  name: 'optionsinput',

  props: {
    name: String,
    initialErrors: {
      type: Array,
      default: () => [],
    },
    initialValue: String,
    watch: {
      type: Boolean,
      default: false,
    },
    optional: Boolean,
    nullOption: {
      type: String,
      default: '',
    },
  },

  data: function() {
    const showError = (this.initialErrors && this.initialErrors.length) || false
    return {
      showError: showError,
      showValid: false,
      validationError: this.initialErrors.join(' '),
      value: this.initialValue,
    }
  },

  methods: {
    onInput: function() {
      this.$parent.$emit('field-change')
    },

    _isValid: function(value) {
      return this.optional || value !== this.nullOption
    },
  },

  computed: {
    valid: function() {
      return this._isValid(this.value)
    },
  },
}
