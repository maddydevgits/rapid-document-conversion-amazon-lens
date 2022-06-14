import streamlit as st
import os
import gtts
import boto3

region='us-east-1'
accessKey='AKIAXHI5XG5NL27XPJNL'
secretAccessKey='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'

st.title('Rapid Document Conversion - Amazon Lens demo')

doc_file=st.file_uploader('Upload doc',type=['.jpg','.png','.jpeg'])

if doc_file is not None:
    file_details={}
    file_details['name']=doc_file.name
    file_details['type']=doc_file.type
    file_details['size']=doc_file.size
    st.write(file_details)

    with open(os.path.join('rdc','src.jpg'),'wb') as f:
        f.write(doc_file.getbuffer())
    
    client=boto3.client('textract',aws_access_key_id=accessKey,aws_secret_access_key=secretAccessKey,region_name=region)
    image=open('rdc/src.jpg','rb')
    response=client.detect_document_text(Document={'Bytes':image.read()})
    #st.write(response)
    text=''
    for item in response["Blocks"]:
        if item["BlockType"]=="LINE":
            lp=(item["Text"])
            st.write(lp)
            text+=lp
            text+=' '
    t1 = gtts.gTTS(text,lang = 'en')
        # save the audio file
    t1.save("welcome.mp3")
    audio_file = open("welcome.mp3",'rb')
    audio_bytes = audio_file.read()
    st.subheader('Audio Output of Text')
    st.audio(audio_bytes, format='audio/ogg', start_time=0)
    



