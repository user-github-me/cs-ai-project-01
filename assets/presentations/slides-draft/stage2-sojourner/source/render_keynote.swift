// Render the concrete PowerPoint with Keynote; do not save or rewrite the source deck.
import Foundation
import AppKit
import CoreText
import PDFKit

let args=CommandLine.arguments
guard args.count==5 else { fatalError("Usage: render_keynote.swift deck.pptx output.pdf Horizon.ttf Quicksand.ttf") }
// Remove only the temporary registrations created during this deck's render setup.
var temporaryFonts=[URL(fileURLWithPath:args[3]),URL(fileURLWithPath:args[4])]
let renderFolder=URL(fileURLWithPath:"/private/tmp/blue-impulse-stage2",isDirectory:true)
if let entries=try? FileManager.default.contentsOfDirectory(at:renderFolder,includingPropertiesForKeys:nil) {
    temporaryFonts += entries.filter { $0.lastPathComponent.hasPrefix("render-Horizon.ttf-") || $0.lastPathComponent.hasPrefix("render-Quicksand-Medium.ttf-") }
}
for url in temporaryFonts {
    var error:Unmanaged<CFError>?
    CTFontManagerUnregisterFontsForURL(url as CFURL,.session,&error)
}
let installedFonts=["BlueImpulse-Horizon.ttf","BlueImpulse-Quicksand.ttf"]
for file in installedFonts {
    let url=FileManager.default.homeDirectoryForCurrentUser.appendingPathComponent("Library/Fonts/"+file)
    var error:Unmanaged<CFError>?
    CTFontManagerRegisterFontsForURL(url as CFURL,.session,&error)
}
// Keynote requires these fonts to be installed; PowerPoint can use the embedded copies.
let requiredFonts=["HorizonPresentation-Bold","Quicksand-Medium"]
for name in requiredFonts {
    guard let font=NSFont(name:name,size:32),font.fontName==name else {
        print("Install the presentation font before rendering with Keynote:",name)
        exit(3)
    }
}
func quoted(_ s:String)->String { "\""+s.replacingOccurrences(of:"\\",with:"\\\\").replacingOccurrences(of:"\"",with:"\\\"")+"\"" }
let restart=Process()
restart.executableURL=URL(fileURLWithPath:"/usr/bin/osascript")
restart.arguments=["-e","if application \"Keynote\" is running then", "-e","tell application \"Keynote\"", "-e","if (count of documents) is 0 then quit", "-e","end tell", "-e","end if"]
try restart.run()
restart.waitUntilExit()
Thread.sleep(forTimeInterval:1)
let launcher=Process()
launcher.executableURL=URL(fileURLWithPath:"/usr/bin/open")
launcher.arguments=["-a","Keynote",args[1]]
try launcher.run()
launcher.waitUntilExit()
Thread.sleep(forTimeInterval:2)
let script="""
with timeout of 300 seconds
    tell application "Keynote"
        set deckDocument to open (POSIX file \(quoted(args[1])))
        delay 3
        export deckDocument to (POSIX file \(quoted(args[2]))) as PDF
        close deckDocument saving no
    end tell
end timeout
"""
let automation=Process()
automation.executableURL=URL(fileURLWithPath:"/usr/bin/osascript")
automation.arguments=["-e",script]
try automation.run()
automation.waitUntilExit()
if automation.terminationStatus != 0 {exit(automation.terminationStatus)}
let pdfBytes=try Data(contentsOf:URL(fileURLWithPath:args[2]))
if String(decoding:pdfBytes,as:UTF8.self).contains("LastResort") {
    print("Native export contains missing-font glyphs; do not publish this PDF.")
    exit(2)
}
guard let pdf=PDFDocument(url:URL(fileURLWithPath:args[2])) else { fatalError("No rendered PDF") }
let directory=URL(fileURLWithPath:"/private/tmp/blue-impulse-stage2/native-previews",isDirectory:true)
try FileManager.default.createDirectory(at:directory,withIntermediateDirectories:true)
for index in 0..<pdf.pageCount {
    guard let page=pdf.page(at:index) else {continue}
    let size=NSSize(width:1920,height:1080)
    let preview=page.thumbnail(of:size,for:.mediaBox)
    guard let tiff=preview.tiffRepresentation,let bitmap=NSBitmapImageRep(data:tiff),
          let jpeg=bitmap.representation(using:.jpeg,properties:[.compressionFactor:0.92]) else {continue}
    try jpeg.write(to:directory.appendingPathComponent(String(format:"slide-%02d.jpg",index+1)))
}
print("Keynote exported \(pdf.pageCount) slides to PDF and rendered native previews.")
