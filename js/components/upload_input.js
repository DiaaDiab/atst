import createNumberMask from 'text-mask-addons/dist/createNumberMask'
import { conformToMask } from 'vue-text-mask'

import { emitEvent } from '../lib/emitters'
import FormMixin from '../mixins/form'
import textinput from './text_input'
import optionsinput from './options_input'

export default {
  name: 'uploadinput',

  mixins: [FormMixin],

  components: {
    textinput,
    optionsinput,
  },

  props: {
    name: String,
    initialData: {
      type: String,
    },
    initialErrors: {
      type: Boolean,
    },
    watch: {
      type: Boolean,
      default: false,
    },
    optional: {
      type: Boolean,
      default: true,
    },
  },

  data: function() {
    return {
      hasInitialData: !!this.initialData,
      attachment: this.initialData || null,
      showErrors: this.initialErrors,
      changed: false,
    }
  },

  created: function() {
    emitEvent('field-mount', this, {
      optional: this.optional,
      name: this.name,
      valid: this.hasAttachment,
    })
  },

  methods: {
    addAttachment: function(e) {
      this.attachment = e.target.value
      this.showErrors = false
      this.changed = true

      emitEvent('field-change', this, {
        value: e.target.value,
        name: this.name,
        watch: this.watch,
        valid: this.hasAttachment,
      })
    },
    removeAttachment: function(e) {
      e.preventDefault()
      this.attachment = null
      if (this.$refs.attachmentInput) {
        this.$refs.attachmentInput.value = null
      }
      this.showErrors = false
      this.changed = true

      emitEvent('field-change', this, {
        value: e.target.value,
        name: this.name,
        watch: this.watch,
      })
    },
  },

  computed: {
    baseName: function() {
      if (this.attachment) {
        return this.attachment.split(/[\\/]/).pop()
      }
    },
    hasAttachment: function() {
      return !!this.attachment
    },
    hideInput: function() {
      return this.hasInitialData && !this.changed
    },
  },
}
