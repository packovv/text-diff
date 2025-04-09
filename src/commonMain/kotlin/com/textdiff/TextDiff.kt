package com.textdiff

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

data class DiffResult(
    val added: List<String>,
    val removed: List<String>,
    val unchanged: List<String>
)

class TextDiff {
    suspend fun compare(text1: String, text2: String): DiffResult = withContext(Dispatchers.Default) {
        val lines1 = text1.lines()
        val lines2 = text2.lines()
        
        val added = mutableListOf<String>()
        val removed = mutableListOf<String>()
        val unchanged = mutableListOf<String>()
        
        var i = 0
        var j = 0
        
        while (i < lines1.size || j < lines2.size) {
            when {
                i >= lines1.size -> {
                    added.add(lines2[j])
                    j++
                }
                j >= lines2.size -> {
                    removed.add(lines1[i])
                    i++
                }
                lines1[i] == lines2[j] -> {
                    unchanged.add(lines1[i])
                    i++
                    j++
                }
                else -> {
                    // Ищем следующее совпадение
                    var found = false
                    for (k in 1..3) {
                        if (i + k < lines1.size && lines1[i + k] == lines2[j]) {
                            for (m in 0 until k) {
                                removed.add(lines1[i + m])
                            }
                            i += k
                            found = true
                            break
                        }
                        if (j + k < lines2.size && lines1[i] == lines2[j + k]) {
                            for (m in 0 until k) {
                                added.add(lines2[j + m])
                            }
                            j += k
                            found = true
                            break
                        }
                    }
                    if (!found) {
                        removed.add(lines1[i])
                        added.add(lines2[j])
                        i++
                        j++
                    }
                }
            }
        }
        
        DiffResult(added, removed, unchanged)
    }
} 