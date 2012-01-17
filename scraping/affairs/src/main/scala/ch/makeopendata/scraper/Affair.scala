package ch.makeopendata.scraper
import org.htmlcleaner.TagNode
import java.io.FileWriter
import java.io.PrintWriter

class Affair(
  val id: String,
  val gsType: String,
  val submitter: String,
  val submitterLink: String,
  val submitterId: String,
  val submissionDate: String,
  val congress: String,
  val state: String,
  val title: String,
  val content: String) {
  def print {
    println("==============================")
    println("Id: " + id)
    println("Type: " + gsType)
    println("Submitted by: " + submitter)
    println("Submitter id: " + submitterId)
    println("Submitter link: " + submitterLink)
    println("Submission date: " + submissionDate)
    println("Congress: " + congress)
    println("State: " + state)
    println("Title: " + title)
    println("Content: " + content)
    println("==============================")
  }
}

object Affair {
  val errorFile = "failures.txt"

  def apply(website: TagNode): Affair = {
    val id = extractId(website)
    val gsType = extractType(website)
    val submitter = extractSubmitter(website)
    val submitterLink = extractSubmitterLink(website)
    val submitterId = submitterLink.split("=").last
    val submissionDate = extractSubmissionDate(website)
    val congress = extractCongress(website)
    val state = extractState(website)
    val title = extractTitle(website)
    val content = extractContent(website)
    new Affair(id, gsType, submitter, submitterLink, submitterId, submissionDate, congress, state, title, content)
  }

  def reportError(text: String) {
    val fileWriter = new FileWriter(errorFile, true)
    val printWriter = new PrintWriter(fileWriter)
    printWriter.println(text)
    fileWriter.close
  }

  def extractTitle(website: TagNode): String = {
    val nodes = website.evaluateXPath("//h3[@class='cv-title']").toList.map(_.asInstanceOf[TagNode])
    if (!nodes.isEmpty) {
      nodes.first.getText.toString
    } else {
      val message = "Extraction failed: field 'title' on website with id: " + extractId(website)
      reportError(message)
      ""
    }
  }

  def extractType(website: TagNode): String = {
    val nodes = website.evaluateXPath(".//*[@id='content']/div[1]/div/h2").toList.map(_.asInstanceOf[TagNode])
    val extracted = nodes.first.getText.toString.split(" \\&ndash; ")
    if (!nodes.isEmpty) {
      if (extracted.size == 2) {
        extracted(1)
      } else {
        val message = "Extraction failed: field 'type' on website with id: " + extractId(website)
        reportError(message)
        ""
      }
    } else {
      val message = "Extraction failed: field 'type' on website with id: " + extractId(website)
      reportError(message)
      ""
    }
  }

  def extractId(website: TagNode): String = {
    val nodes = website.evaluateXPath("//*[@id='content']/div[1]/div/h2").toList.map(_.asInstanceOf[TagNode])
    if (!nodes.isEmpty) {
      val extracted = nodes.first.getText.toString.split(" \\&ndash; ")
      if (!extracted.isEmpty) {
        extracted.first
      } else {
        val message = "Extraction failed: field 'id' on website: " + website
        reportError(message)
        ""
      }
    } else {
      val message = "Extraction failed: field 'id' on website: " + website
      reportError(message)
      ""
    }
  }

  def extractSubmitter(website: TagNode): String = {
    val nodes = website.evaluateXPath("//*[@id='content']/div[1]/div/dl/dd[1]/ul/li/a/span").toList.map(_.asInstanceOf[TagNode])
    if (!nodes.isEmpty) {
      nodes.first.getText.toString
    } else {
      val message = "Extraction failed: field 'submitter' on website with id: " + extractId(website)
      reportError(message)
      ""
    }
  }

  def extractContent(website: TagNode): String = {
    val nodes = website.evaluateXPath("//*[@id='content']/div[4]").toList.map(_.asInstanceOf[TagNode])
    if (!nodes.isEmpty) {
      val content = nodes.first.getText.toString
      if (content.size > 18) {
        content.substring(18)
      } else {
        content
      }
    } else {
      val message = "Extraction failed: field 'content' on website with id: " + extractId(website)
      reportError(message)
      ""
    }
  }

  def extractSubmissionDate(website: TagNode): String = {
    val summaryItemsCount = website.evaluateXPath("//*[@id='content']/div[1]/div/dl/dd").toList.length
    val index = summaryItemsCount - 2
    val nodes = website.evaluateXPath("//*[@id='content']/div[1]/div/dl/dd[" + index + "]").toList.map(_.asInstanceOf[TagNode])

    if (!nodes.isEmpty) {
      nodes.first.getText.toString
    } else {
      val message = "Extraction failed: field 'sumbission date' on website with id: " + extractId(website)
      reportError(message)
      ""
    }
  }

  def extractCongress(website: TagNode): String = {
    val summaryItemsCount = website.evaluateXPath("//*[@id='content']/div[1]/div/dl/dd").toList.length
    val index = summaryItemsCount - 1
    val nodes = website.evaluateXPath("//*[@id='content']/div[1]/div/dl/dd[" + index + "]").toList.map(_.asInstanceOf[TagNode])
    if (!nodes.isEmpty) {
      nodes.first.getText.toString
    } else {
      val message = "Extraction failed: field 'congress' on website with id: " + extractId(website)
      reportError(message)
      ""
    }
  }

  def extractState(website: TagNode): String = {
    val summaryItemsCount = website.evaluateXPath("//*[@id='content']/div[1]/div/dl/dd").toList.length
    val nodes = website.evaluateXPath("//*[@id='content']/div[1]/div/dl/dd[" + summaryItemsCount + "]").toList.map(_.asInstanceOf[TagNode])
    if (!nodes.isEmpty) {
      nodes.first.getText.toString
    } else {
      val message = "Extraction failed: field 'state' on website with id: " + extractId(website)
      reportError(message)
      ""
    }
  }

  def extractSubmitterLink(website: TagNode): String = {
    val nodes = website.evaluateXPath("//*[@id='content']/div[1]/div/dl/dd[1]/ul/li/a/@href").toList
    if (!nodes.isEmpty) {
      "http://www.parlament.ch/" + nodes.first.toString
    } else {
      val message = "Extraction failed: field 'submitter link' on website with id: " + extractId(website)
      reportError(message)
      ""
    }

  }

}
