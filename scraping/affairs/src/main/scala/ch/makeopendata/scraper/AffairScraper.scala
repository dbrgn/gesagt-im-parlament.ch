package ch.makeopendata.scraper

import org.htmlcleaner.HtmlCleaner
import org.htmlcleaner.TagNode
import java.net.URL
import java.net.HttpURLConnection
import com.google.gson.Gson
import java.io.FileWriter
import java.io.PrintWriter

object AffairScraper extends App {

  val fileName = "affairs.json"

  val gson = new Gson

  for (year <- 2012 to 1996 by -1) {
    for (gsType <- 1 to 5) {
      var failureCount = 0
      for (gs <- 0 to 999) {
        if (failureCount < 10) {
          val realGsId = "%03d".format(gs)
          val gsIdPart = year.toString + gsType.toString + realGsId
          val url = "http://www.parlament.ch/d/suche/seiten/geschaefte.aspx?gesch_id=" + gsIdPart
          try {
            val website = io.Source.fromURL(url, "UTF-8").mkString
            if (!website.contains("Es wurde kein Geschäft mit dieser ID gefunden.")) {
              val cleaner = new HtmlCleaner
              val node = cleaner.clean(website)
              val affair = Affair(node)
              if (affair.submitter.size > 0) {
                val json = gson.toJson(affair)
                println(gsIdPart + " saved (title: \"" + affair.title + "\")")
                append(fileName, json)
              } else {
                println(gsIdPart + " was not submitted by a member of NR/SR - discarded")
              }
            } else {
              failureCount += 1
            }
          } catch {
            case e: Throwable => {
              failureCount += 1
              println("Failed to load url: " + url + " if this is due to connectivity issues, please resume @ id " + gsIdPart + " error: " + e)
            }
          }
        }
      }
    }
  }

  def append(fileName: String, text: String) {
    val fileWriter = new FileWriter(fileName, true)
    val printWriter = new PrintWriter(fileWriter)
    printWriter.println(text)
    fileWriter.close
  }

}
