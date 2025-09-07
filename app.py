# Combine all text for sentiment and word cloud
combined_text = " ".join(news_texts)

if combined_text.strip():  # Only proceed if there is text
    # Sentiment analysis
    sentiment_score = TextBlob(combined_text).sentiment.polarity
    st.subheader("Overall Sentiment Score")
    st.write(sentiment_score)

    # Word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
    
    # Downloadable report
    report_text = f"Company: {company_name}\n\nSentiment Score: {sentiment_score}\n\nNews Articles:\n"
    report_text += "\n".join(news_texts)
    st.download_button("Download Report", report_text, file_name=f"{company_name}_HR_report.txt")
else:
    st.write("No news articles found. Word cloud and sentiment analysis cannot be generated.")
