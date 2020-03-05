const colType = { Object, Array }

function pathToString(path) {
  let s = '$'
  try {
    for (const frame of path) {
      if (frame.colType === colType.Object) {
        if (!frame.key.match(/^[a-zA-Z$_][a-zA-Z\d$_]*$/)) {
          s += `["${frame.key}"]`
        } else {
          if (s.length) {
            s += '.'
          }
          s += frame.key
        }
      } else {
        s += `[${frame.index}]`
      }
    }
    return s
  } catch (ex) {
    return ''
  }
}

function isEven(n) {
  return n % 2 === 0
}

// Find the next end quote
function findEndQuote(text, i) {
  while (i < text.length) {
    if (text[i] === '"') {
      let bt = i
      // Handle backtracking to find if this quote escaped (or, if the escape is escaping a slash)
      while (bt >= 0 && text[bt] === '\\') {
        bt -= 1
      }
      if (isEven(i - bt)) {
        break
      }
    }
    i += 1
  }
  return i
}

function readString(text, pos) {
  let i = pos + 1
  i = findEndQuote(text, i)
  const textpos = {
    text: text.substring(pos + 1, i),
    pos: i + 1,
  }
  return textpos
}

function getJsonPath(text, offSet) {
  let pos = 0
  const stack = []
  let isInKey = false
  while (pos < offSet) {
    const startPos = pos
    let s = null
    let newPos = null
    let readStringReturnObj = null
    switch (text[pos]) {
      case '"':
        readStringReturnObj = readString(text, pos)
        s = readStringReturnObj.text
        newPos = readStringReturnObj.pos
        if (stack.length) {
          const frame = stack[stack.length - 1]
          if (frame.colType === colType.Object && isInKey) {
            frame.key = s
            isInKey = false
          }
        }
        pos = newPos
        break
      case '{':
        stack.push({ colType: colType.Object })
        isInKey = true
        break
      case '[':
        stack.push({ colType: colType.Array, index: 0 })
        break
      case '}':
      case ']':
        stack.pop()
        break
      case ',':
        if (stack.length) {
          const frame = stack[stack.length - 1]
          if (frame.colType === colType.Object) {
            isInKey = true
          } else {
            frame.index += 1
          }
        }
        break
      default:
        break
    }
    if (pos === startPos) {
      pos += 1
    }
  }
  return pathToString(stack)
}

export default getJsonPath
