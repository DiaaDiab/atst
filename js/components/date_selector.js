import Vue from 'vue'
import { getDaysInMonth } from 'date-fns'

var paddedNumber = function(number) {
  if ((number + '').length === 1) {
    return `0${number}`
  } else {
    return number
  }
}

export default {
  name: 'date-selector',

  props: {
    initialday: { type: String },
    initialmonth: { type: String },
    initialyear: { type: String },
    mindate: { type: String },
    maxdate: { type: String },
  },

  data: function() {
    return {
      day: this.initialday,
      month: this.initialmonth,
      year: this.initialyear,
    }
  },

  watch: {
    month(newMonth, oldMonth) {
      if (!!newMonth && newMonth.length > 2) {
        this.month = oldMonth
      }
    },

    day(newDay, oldDay) {
      if (!!newDay && newDay.length > 2) {
        this.day = oldDay
      }
    },

    year(newYear, oldYear) {
      if (!!newYear && newYear.length > 4) {
        this.year = oldYear
      }
    },
  },

  computed: {
    formattedDate: function() {
      let day = paddedNumber(this.day)
      let month = paddedNumber(this.month)

      if (!day || !month || !this.year) {
        return null
      }

      return `${month}/${day}/${this.year}`
    },

    isMonthValid: function() {
      var _month = parseInt(this.month)
      var valid = _month >= 0 && _month <= 12
      this._emitChange('month', this.month, valid)
      return valid
    },

    isDayValid: function() {
      var _day = parseInt(this.day)
      var valid = _day >= 0 && _day <= this.daysMaxCalculation
      this._emitChange('day', this.day, valid)
      return valid
    },

    isYearValid: function() {
      // Emit a change event
      var valid = parseInt(this.year) >= 1
      this._emitChange('year', this.year, valid)
      return valid
    },

    isWithinDateRange: function() {
      let _mindate = this.mindate ? Date.parse(this.mindate) : null
      let _maxdate = this.maxdate ? Date.parse(this.maxdate) : null
      let _dateTimestamp = Date.UTC(this.year, this.month - 1, this.day)

      if (_mindate !== null && _mindate >= _dateTimestamp) {
        return false
      }

      if (_maxdate !== null && _maxdate <= _dateTimestamp) {
        return false
      }

      return true
    },

    isDateValid: function() {
      return (
        this.day &&
        this.month &&
        this.year &&
        this.isDayValid &&
        this.isMonthValid &&
        this.isYearValid &&
        this.isWithinDateRange
      )
    },

    daysMaxCalculation: function() {
      switch (parseInt(this.month)) {
        case 2: // February
          if (this.year) {
            return getDaysInMonth(new Date(this.year, this.month - 1))
          } else {
            return 29
          }
          break

        case 4: // April
        case 6: // June
        case 9: // September
        case 11: // November
          return 30
          break

        default:
          // All other months, or null, go with 31
          return 31
      }
    },
  },

  methods: {
    _emitChange: function(name, value, valid) {
      this.$root.$emit('field-change', {
        value,
        name,
        parent_uid: this.$parent && this.$parent._uid,
      })
    },
  },

  render: function(createElement) {
    return createElement('p', 'Please implement inline-template')
  },
}
