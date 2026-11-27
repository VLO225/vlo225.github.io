# Points each page's X/Twitter preview at a generated share card (see _cards/make_cards.py)
# when it has no cover image of its own. The card is only used for previews, never shown on the page.
Jekyll::Hooks.register :site, :post_read do |site|
  base = File.join(site.source, "cards")
  site.collections["entries"]&.docs&.each do |doc|
    next if doc.data["image"]
    card = "/cards/#{doc.basename_without_ext}.png"
    next unless File.exist?(File.join(base, "#{doc.basename_without_ext}.png"))
    doc.data["image"] = card
    doc.data["auto_card"] = true
  end
  if File.exist?(File.join(base, "site.png"))
    site.pages.each do |page|
      next if page.data["image"] || !page.html?
      page.data["image"] = "/cards/site.png"
      page.data["auto_card"] = true
    end
  end
end
